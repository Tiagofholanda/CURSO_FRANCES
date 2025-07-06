import streamlit as st
import pandas as pd
from auth import auth_required
from utils.module_utils import get_module_lessons, apply_responsive_styles, display_progress_bar
from utils.excel_utils import load_excel_from_google_drive
from utils.progress_utils import save_progress, is_lesson_completed, get_module_progress

# Verifica autenticação
auth_required()

# Configuração da página
st.set_page_config(
    page_title="Vocabulário - Curso de Francês",
    page_icon="📚",
    layout="wide"
)

# URL da planilha
SPREADSHEET_URL = "https://docs.google.com/spreadsheets/d/1RWd50uSh5AOTloRCXvIKPU9jBEUf4LI3/edit?usp=sharing"
MODULE_NAME = "Vocabulário"

def get_vocabulary_lessons():
    """Busca as lições de vocabulário na planilha"""
    try:
        # Carrega os dados da planilha
        df = load_excel_from_google_drive(SPREADSHEET_URL)
        
        # Verifica se o DataFrame está vazio
        if df.empty:
            st.warning("A planilha está vazia ou não pôde ser carregada.")
            return {}
            
        # Verifica se as colunas necessárias existem
        required_columns = ['Módulo', 'ordem', 'Título da Aula', 'Duração', 'Link do Vídeo', 'Link do Documento']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            st.error(f"Colunas ausentes na planilha: {', '.join(missing_columns)}")
            return {}
            
        # Remove linhas onde o Módulo está vazio
        df = df.dropna(subset=['Módulo'])
        
        # Converte para string e remove espaços extras
        df['Módulo'] = df['Módulo'].astype(str).str.strip()
        
        # Filtra apenas as lições de vocabulário (case insensitive)
        vocabulario_df = df[df['Módulo'].str.lower() == MODULE_NAME.lower()]
        
        if vocabulario_df.empty:
            st.warning(f"Nenhuma lição de {MODULE_NAME.lower()} encontrada na planilha.")
            return {}
            
        # Preenche valores vazios
        vocabulario_df = vocabulario_df.fillna('')
        
        # Cria a estrutura de módulos
        modules = {}
        modules[MODULE_NAME] = []
        
        # Adiciona as lições
        for _, row in vocabulario_df.iterrows():
            try:
                # Obtém a ordem, garantindo que seja um número inteiro
                try:
                    ordem = int(float(str(row['ordem']).strip() or '0'))
                except (ValueError, AttributeError):
                    ordem = 0
                    
                # Obtém o título, garantindo que seja uma string
                titulo = str(row['Título da Aula']).strip()
                if not titulo:
                    titulo = f"Liçao {ordem}"
                    
                # Verifica se a coluna 'link extra youtube' existe no DataFrame
                youtube_url = ''
                if 'link extra youtube' in row:
                    youtube_url = str(row['link extra youtube']).strip()
                    
                modules[MODULE_NAME].append({
                    'title': titulo,
                    'video_url': str(row['Link do Vídeo']).strip(),
                    'doc_url': str(row['Link do Documento']).strip(),
                    'youtube_url': youtube_url,
                    'duration': str(row['Duração']).strip(),
                    'order': ordem,
                    'id': f"vocab_{ordem}"
                })
                
            except Exception as e:
                st.warning(f"Erro ao processar linha da planilha: {str(e)}")
                continue
        
        # Ordena as lições pela ordem
        if MODULE_NAME in modules:
            modules[MODULE_NAME].sort(key=lambda x: x['order'])
            
        return {'lessons': modules[MODULE_NAME]}
        
    except Exception as e:
        st.error(f"Erro ao carregar as lições: {str(e)}")
        import traceback
        st.error(traceback.format_exc())
        return {}

# Aplicar estilos responsivos
apply_responsive_styles()

# Conteúdo da página
st.markdown(f"""
## Aprenda o Vocabulário Francês

Nesta seção, você encontrará lições com vocabulário essencial em francês para melhorar sua comunicação.
""")

def display_vocabulary_lessons():
    """Exibe as lições de vocabulário"""
    modules = get_vocabulary_lessons()
    
    if not modules or 'lessons' not in modules:
        st.warning(f"Nenhuma lição de {MODULE_NAME.lower()} encontrada.")
        return
    
    lessons = modules['lessons']
    module_id = MODULE_NAME.lower()
    
    # Exibe a barra de progresso
    progress = get_module_progress(module_id, len(lessons))
    display_progress_bar(module_id, len(lessons), progress)
    
    # Exibe as lições
    st.markdown("## 📋 Lições Disponíveis")
    
    for lesson in lessons:
        lesson_id = lesson.get('id')
        is_completed = is_lesson_completed(module_id, lesson_id)
        
        # Estilo para lições concluídas
        expander_style = ""
        if is_completed:
            expander_style = """
                <style>
                    div[data-testid="stExpander"][data-test-state*="expanded"] {
                        border-left: 5px solid #4CAF50;
                        padding-left: 10px;
                    }
                    div[data-testid="stExpander"] > div[role="button"] > div:first-child > div:first-child::before {
                        content: '✓ ';
                        color: #4CAF50;
                        font-weight: bold;
                    }
                </style>
            """
            st.markdown(expander_style, unsafe_allow_html=True)
        
        with st.expander(f"📚 {lesson.get('title', 'Sem título')} ({lesson.get('duration', '')})", 
                        expanded=is_completed):
            # Vídeo
            video_url = str(lesson.get('video_url', '')).strip()
            if video_url and video_url.lower() not in ['nan', 'none', '']:
                st.markdown("### 🎥 Assista à Aula")
                try:
                    from utils.video_security import get_secure_video_embed
                    secure_embed = get_secure_video_embed(video_url)
                    st.markdown(secure_embed, unsafe_allow_html=True)
                except Exception as e:
                    st.warning(f"Não foi possível carregar o vídeo: {str(e)}")
            
            # Material de Apoio
            doc_url = str(lesson.get('doc_url', '')).strip()
            if doc_url and doc_url.lower() not in ['nan', 'none', '']:
                st.markdown("### 📄 Material de Apoio")
                try:
                    file_id = doc_url.split('/file/d/')[1].split('/')[0]
                    download_url = f"https://drive.google.com/uc?export=download&id={file_id}"
                    st.markdown(
                        f'<a href="{download_url}" '
                        'style="display: inline-flex; align-items: center; background-color: #1E88E5; color: white; '
                        'padding: 10px 20px; border-radius: 4px; text-decoration: none; font-weight: bold; margin: 10px 0;" '
                        'target="_blank">'
                        '📥 Baixar Material</a>',
                        unsafe_allow_html=True
                    )
                except Exception as e:
                    st.warning(f"Link de documento inválido: {str(e)}")
            
            # Link do YouTube
            youtube_url = str(lesson.get('youtube_url', '')).strip()
            if youtube_url and youtube_url.lower() not in ['nan', 'none', '']:
                st.markdown("### 🎥 Vídeo Extra no YouTube")
                try:
                    st.markdown(
                        f'<a href="{youtube_url}" '
                        'style="display: inline-flex; align-items: center; background-color: #FF0000; color: white; '
                        'padding: 10px 20px; border-radius: 4px; text-decoration: none; font-weight: bold; margin: 10px 0;" '
                        'target="_blank">'
                        '▶️ Assistir no YouTube</a>',
                        unsafe_allow_html=True
                    )
                except Exception as e:
                    st.warning(f"Link do YouTube inválido: {str(e)}")
            
            # Botão de conclusão
            col1, col2 = st.columns([1, 3])
            with col1:
                button_text = "✅ Concluído" if is_completed else "✅ Marcar como concluída"
                button_type = "primary" if is_completed else "secondary"
                
                if st.button(button_text, 
                           key=f"complete_{lesson_id}",
                           type=button_type):
                    # Salva o estado de conclusão da lição
                    save_progress(module_id, lesson_id, not is_completed)
                    st.rerun()

# Exibe as lições
display_vocabulary_lessons()
