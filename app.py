# app.py
import streamlit as st
import pandas as pd
import requests
from io import BytesIO
import json
import os
from utils.module_utils import get_modules_data
from utils.excel_utils import load_excel_from_google_drive
from auth import login, auth_required, logout

# Configuração da página
st.set_page_config(
    page_title="Curso de Francês",
    page_icon="🇫🇷",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Esconde o menu de tema
hide_menu_style = """
    <style>
        #MainMenu {visibility: hidden;}
        header {visibility: hidden;}
        .css-1d391kg {display: none;}
    </style>
"""
st.markdown(hide_menu_style, unsafe_allow_html=True)

# Importa as configurações de segurança
from utils.security import set_security_headers

# Configura os cabeçalhos de segurança
set_security_headers()

# Adiciona o arquivo JavaScript personalizado
def add_js():
    try:
        with open("assets/script.js") as f:
            st.components.v1.html(f"""
            <script>
            {f.read()}
            </script>
            """, height=0)
    except Exception as e:
        st.error(f"Erro ao carregar o JavaScript: {str(e)}")

# Adiciona o JavaScript à página
add_js()

# Inicializa a sessão se não existir
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.username = ''
    st.session_state.role = ''

# Caminho para o arquivo local
import os
EXCEL_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), "video_curso.xlsx"))
print(f"Tentando carregar o arquivo em: {EXCEL_FILE}")
print(f"Arquivo existe: {os.path.exists(EXCEL_FILE)}")

# Configurações de depuração
DEBUG_MODE = True  # Defina como False em produção

# Função simplificada para carregar os dados
def load_data(file_path):
    try:
        print(f"Carregando dados diretamente do Excel: {file_path}")
        # Lê o arquivo Excel diretamente a cada chamada
        df = pd.read_excel(file_path, engine='openpyxl')
        print(f"Colunas encontradas: {df.columns.tolist()}")
        print(f"Total de linhas: {len(df)}")
        
        # Verifica colunas obrigatórias
        required_columns = ['Módulo', 'Título da Aula', 'Link do Vídeo']
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            print(f"Aviso: Colunas obrigatórias ausentes: {missing_columns}")
            return None
        
        # Preenche valores vazios com string vazia
        df = df.fillna('')
        
        # Remove linhas sem link de vídeo
        df = df[df['Link do Vídeo'].astype(str).str.strip() != '']
        
        if len(df) == 0:
            print("Aviso: Nenhuma linha com link de vídeo válido encontrada")
            return None
            
        print(f"Total de aulas após filtragem: {len(df)}")
        
        # Converte para o formato esperado
        modules = {}
        for _, row in df.iterrows():
            try:
                module_name = str(row['Módulo']).strip() if row['Módulo'] else "Outros"
                if module_name not in modules:
                    modules[module_name] = []
                
                # Extrai o ID do vídeo do YouTube se disponível
                youtube_url = str(row.get('link extra youtube', '')).strip()
                youtube_id = None
                if 'youtube.com' in youtube_url or 'youtu.be' in youtube_url:
                    if 'youtu.be' in youtube_url:
                        youtube_id = youtube_url.split('/')[-1].split('?')[0]
                    else:
                        youtube_id = youtube_url.split('v=')[1].split('&')[0]
                
                lesson_data = {
                    'id': str(row.get('ID', '')).strip(),
                    'title': str(row['Título da Aula']).strip() if row['Título da Aula'] else "Sem título",
                    'video_url': str(row['Link do Vídeo']).strip(),
                    'doc_url': str(row.get('Link do Documento', '')).strip(),
                    'youtube_url': youtube_url,
                    'youtube_id': youtube_id,
                    'duration': str(row.get('Duração', '')).strip(),
                    'order': int(row.get('ordem', 0)) if str(row.get('ordem', '0')).isdigit() else 0
                }
                
                modules[module_name].append(lesson_data)
                
            except Exception as e:
                print(f"Erro ao processar linha {_}: {str(e)}")
                continue
            
        # Ordena os itens
        for module in modules:
            modules[module].sort(key=lambda x: x.get('order', 0))
            
        return modules
        
    except Exception as e:
        print(f"Erro ao carregar dados: {str(e)}")
        import traceback
        print(traceback.format_exc())
        return None

# Verifica se estamos na página de introdução
current_page = st.query_params.get('page', [''])[0]
is_intro_page = '00_Introdução' in current_page

# Se não estiver autenticado e não estiver na página de introdução
if not st.session_state.authenticated and not is_intro_page:
    # Usa st.rerun para garantir que o redirecionamento aconteça após a inicialização
    st.query_params.page = '00_Introdução'
    st.rerun()

# Se estiver na página de introdução, não renderiza o resto do app
if is_intro_page:
    st.stop()

# Barra lateral com menu de navegação
st.sidebar.title(f"Olá, {st.session_state.username}")

# Menu de navegação
st.sidebar.markdown("### Navegação")
page = st.sidebar.radio(
    "Selecione uma seção:",
    ["Introdução", "Módulos do Curso", "Vocabulário", "Pronúncia", "Gramática"]
)

# Navegação entre páginas
if page == "Introdução":
    st.switch_page("pages/00_Introdução.py")
elif page == "Vocabulário":
    st.switch_page("pages/01_Vocabulário.py")
elif page == "Pronúncia":
    st.switch_page("pages/02_Pronúncia.py")
elif page == "Gramática":
    st.switch_page("pages/03_Gramática.py")

# Botão de logout
if st.sidebar.button(" Sair"):
    logout()

# Carrega os dados
try:
    with st.spinner('Carregando dados do curso...'):
        modules_data = load_data(EXCEL_FILE)
        
        if not modules_data:
            st.error("❌ Não foi possível carregar os dados do curso. Verifique o arquivo de log para mais detalhes.")
            st.stop()
            
    print(f"Módulos carregados: {list(modules_data.keys())}")
    
except Exception as e:
    st.error(f"❌ Erro ao carregar os dados: {str(e)}")
    print(f"Erro detalhado: {str(e)}")
    import traceback
    traceback.print_exc()
    st.stop()

# Barra lateral para navegação
st.sidebar.title("Navegação")

# Lista de módulos para seleção
selected_module = st.sidebar.selectbox(
    "Selecione o Módulo",
    list(modules_data.keys()) if modules_data else ["Nenhum módulo disponível"]
)

# Exibe o conteúdo do módulo selecionado
st.title(f"Módulo: {selected_module}")

# Seção especial para a introdução
if selected_module == "Introdução":
    st.markdown("""
    <div style="background-color: #f8f9fa; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
        <h2 style="color: #2c3e50; margin-top: 0;">👋 Bem-vindo ao Curso de Francês!</h2>
        <p style="color: #34495e; font-size: 1.1em;">Neste módulo introdutório, você terá acesso a materiais importantes para começar seus estudos.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Cria duas colunas para melhor organização
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Vídeo da introdução (opcional)
        st.markdown("### 🎥 Vídeo de Introdução")
        
        # Seção de configuração do vídeo
        with st.expander("🔧 Configurações do Vídeo", expanded=False):
            st.info("Para adicionar um vídeo:")
            st.markdown("""
            1. Envie seu vídeo para o Google Drive
            2. Compartilhe o vídeo como "Qualquer pessoa com o link pode visualizar"
            3. Cole o ID do vídeo abaixo (o código após '/d/' na URL)
            """)
            
            # Campo para o usuário colar o ID do vídeo
            video_id = st.text_input("ID do Vídeo do Google Drive", 
                                  value="", 
                                  placeholder="Ex: 1WiHVX6lWQ87d7e-v54zo0FCwewNR8_B4")
            
            # Botão para testar o vídeo
            if st.button("Testar Vídeo") and video_id:
                try:
                    # Testa se o vídeo está acessível
                    test_url = f"https://drive.google.com/file/d/{video_id}/preview"
                    st.markdown(f"""
                    <div style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; border-radius: 8px; margin: 10px 0; background: #f0f2f6;">
                        <iframe 
                            src="{test_url}" 
                            style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: none;" 
                            frameborder="0"
                            allowfullscreen>
                        </iframe>
                    </div>
                    """, unsafe_allow_html=True)
                    st.success("Vídeo carregado com sucesso!")
                    
                except Exception as e:
                    st.error("Não foi possível carregar o vídeo. Verifique o ID e as permissões.")
        
        # Seção principal do vídeo
        if 'intro_video_id' in st.session_state and st.session_state.intro_video_id:
            try:
                video_id = st.session_state.intro_video_id
                intro_video_embed = f"""
                <div style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; border-radius: 8px; margin: 10px 0; background: #f0f2f6; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                    <iframe 
                        src="https://drive.google.com/file/d/{video_id}/preview" 
                        style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: none;" 
                        frameborder="0"
                        allowfullscreen>
                    </iframe>
                </div>
                <div style="margin: 10px 0 20px 0;">
                    <a href="https://drive.google.com/file/d/{video_id}/view" 
                       target="_blank" 
                       rel="noopener noreferrer"
                       style="display: inline-block; padding: 8px 16px; background: #f1f3f4; border-radius: 4px; text-decoration: none; color: #1a73e8; font-weight: 500; margin-right: 10px;">
                        🔗 Abrir no Google Drive
                    </a>
                    <a href="https://drive.google.com/uc?export=download&id={video_id}" 
                       target="_blank"
                       style="display: inline-block; padding: 8px 16px; background: #1a73e8; color: white; border-radius: 4px; text-decoration: none; font-weight: 500;">
                        ⬇️ Baixar Vídeo
                    </a>
                </div>
                """
                st.markdown(intro_video_embed, unsafe_allow_html=True)
                
            except Exception as e:
                st.warning("""
                **Atenção:** Não foi possível carregar o vídeo.
                
                Por favor, verifique:
                - Se o ID do vídeo está correto
                - Se o vídeo está configurado como "Qualquer pessoa com o link pode visualizar"
                - Sua conexão com a internet
                """)
        else:
            st.info("ℹ️ Nenhum vídeo configurado. Use a seção de configurações acima para adicionar um vídeo.")
            st.markdown("""
            <div style="padding: 15px; background: #e3f2fd; border-radius: 8px; margin: 10px 0 20px 0;">
                <p style="margin: 0; color: #0d47a1;">
                    <strong>Dica:</strong> Se não tiver um vídeo, você pode pular esta seção ou adicionar um vídeo posteriormente.
                </p>
            </div>
            """, unsafe_allow_html=True)
        st.markdown(intro_video_embed, unsafe_allow_html=True)
        
        # Espaço para anotações
        st.markdown("### 📝 Anotações Pessoais")
        intro_note_key = "note_introducao_geral"
        if intro_note_key not in st.session_state:
            st.session_state[intro_note_key] = ""
        
        st.session_state[intro_note_key] = st.text_area(
            "Faça suas anotações aqui:",
            value=st.session_state[intro_note_key],
            height=200,
            key="intro_textarea",
            label_visibility="collapsed",
            placeholder="Anote suas observações, dúvidas ou pontos importantes sobre a introdução..."
        )
    
    with col2:
        # Documento da introdução
        st.markdown("### 📚 Material de Apoio")
        intro_doc_id = "1bZSa8HZrrT1zzjkLhXwGq-UrKLDglkSr"
        intro_doc_embed = f"""
        <div style="position: relative; padding-bottom: 140%; height: 0; overflow: hidden; border-radius: 8px; margin: 10px 0; border: 1px solid #e0e0e0; background: #ffffff; box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
            <iframe 
                src="https://docs.google.com/viewer?url=https://drive.google.com/uc?export=download&id={intro_doc_id}&embedded=true"
                style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: none;" 
                frameborder="0"
                allowfullscreen
                sandbox="allow-same-origin allow-scripts allow-popups">
            </iframe>
        </div>
        <div style="display: flex; flex-direction: column; gap: 8px; margin-top: 10px;">
            <a href="https://drive.google.com/file/d/1bZSa8HZrrT1zzjkLhXwGq-UrKLDglkSr/view" 
               target="_blank" 
               rel="noopener noreferrer"
               style="display: block; text-align: center; background-color: #f1f3f4; padding: 10px; border-radius: 4px; text-decoration: none; color: #202124; font-weight: 500; font-size: 0.9em;">
                👁️ Visualizar no Google Drive
            </a>
            <a href="https://drive.google.com/uc?export=download&id=1bZSa8HZrrT1zzjkLhXwGq-UrKLDglkSr" 
               target="_blank" 
               rel="noopener noreferrer"
               style="display: block; text-align: center; background-color: #1a73e8; color: white; padding: 10px; border-radius: 4px; text-decoration: none; font-weight: 500; font-size: 0.9em;">
                ⬇️ Baixar Material
            </a>
        </div>
        """
        st.markdown(intro_doc_embed, unsafe_allow_html=True)
    
    # Divisor antes das aulas
    st.markdown("---")
    st.markdown("## 📋 Aulas do Módulo")
    st.markdown("Confira abaixo as aulas disponíveis neste módulo:")
    st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)

# Ordena as aulas pelo campo 'order'
sorted_lessons = sorted(modules_data[selected_module], key=lambda x: x.get('order', 0))

# Exibe as aulas do módulo
for lesson in sorted_lessons:
    with st.expander(f"📹 {lesson['title']} ({lesson.get('duration', '')})", expanded=False):
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Mostra o vídeo do YouTube se disponível, senão mostra o vídeo do Google Drive
            if lesson.get('youtube_id'):
                st.markdown("### 🎥 Vídeo da Aula (YouTube)")
                youtube_embed = f"""
                <div style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; border-radius: 8px; margin: 10px 0;">
                    <iframe 
                        src="https://www.youtube.com/embed/{lesson['youtube_id']}?rel=0&modestbranding=1&showinfo=0" 
                        style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: none;" 
                        frameborder="0" 
                        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
                        allowfullscreen>
                    </iframe>
                </div>
                """
                st.markdown(youtube_embed, unsafe_allow_html=True)
                
                # Mostra o link do YouTube
                st.markdown(f"🔗 [Assistir no YouTube]({lesson['youtube_url']})")
            
            # Mostra o vídeo do Google Drive se disponível
            video_url = str(lesson['video_url']).strip()
            if video_url and video_url.lower() not in ['nan', 'none', '']:
                if not lesson.get('youtube_id'):  # Só mostra se não tiver vídeo do YouTube
                    st.markdown("### 🎥 Vídeo da Aula")
                    try:
                        from utils.video_security import get_secure_video_embed
                        secure_embed = get_secure_video_embed(video_url)
                        st.markdown(secure_embed, unsafe_allow_html=True)
                    except Exception as e:
                        st.error(f"❌ Erro ao carregar o vídeo: {str(e)}")
            
            if not lesson.get('youtube_id') and (not video_url or video_url.lower() in ['nan', 'none', '']):
                st.warning("⚠️ Link de vídeo não disponível.")
        
        with col2:
            # Mostra o link para baixar o documento, se disponível
            doc_url = str(lesson.get('doc_url', '')).strip()
            if doc_url and doc_url.lower() not in ['nan', 'none', '']:
                st.markdown("### 📚 Material de Apoio")
                
                if 'drive.google.com' in doc_url and '/file/d/' in doc_url:
                    file_id = doc_url.split('/file/d/')[1].split('/')[0]
                    preview_url = f"https://drive.google.com/file/d/{file_id}/preview"
                    download_url = f"https://drive.google.com/uc?export=download&id={file_id}"
                    
                    # Mostra o documento em um iframe
                    st.markdown(f"""
                    <div style="position: relative; padding-bottom: 130%; height: 0; overflow: hidden; border-radius: 8px; margin: 10px 0; border: 1px solid #e0e0e0;">
                        <iframe 
                            src="{preview_url}" 
                            style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: none;" 
                            frameborder="0" 
                            allow="autoplay">
                        </iframe>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Botão para baixar o documento
                    st.markdown(f"""
                    <a href="{download_url}" target="_blank" style="text-decoration: none;">
                        <button style="background-color: #4CAF50; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; width: 100%;">
                            📥 Baixar Material
                        </button>
                    </a>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <a href="{doc_url}" target="_blank" style="text-decoration: none;">
                        <button style="background-color: #4CAF50; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; width: 100%;">
                            📥 Baixar Material
                        </button>
                    </a>
                    """, unsafe_allow_html=True)
            
            # Adiciona espaço para anotações
            st.markdown("### 📝 Anotações")
            note_key = f"note_{selected_module}_{lesson['title']}"
            if note_key not in st.session_state:
                st.session_state[note_key] = ""
                
            st.session_state[note_key] = st.text_area(
                "Faça suas anotações aqui:",
                value=st.session_state[note_key],
                height=200,
                key=f"textarea_{note_key}",
                label_visibility="collapsed"
            )

# Espaço no final da página
st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)
