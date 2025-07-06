import streamlit as st
import pandas as pd
from auth import auth_required
from utils.module_utils import get_modules_data
from utils.excel_utils import load_excel_from_google_drive

# Verifica autenticação
auth_required()

# Configuração da página
st.set_page_config(page_title="Gramática - Curso de Francês", layout="wide")

# Título da página
st.title("Gramática Francesa")

# URL da planilha
SPREADSHEET_URL = "https://docs.google.com/spreadsheets/d/1RWd50uSh5AOTloRCXvIKPU9jBEUf4LI3/edit?usp=sharing"

def get_grammar_lessons():
    """Busca as lições de gramática na planilha"""
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
        
        # Filtra apenas as lições de gramática (case insensitive)
        gramatica_df = df[df['Módulo'].str.lower() == 'gramática']
        
        if gramatica_df.empty:
            st.warning("Nenhuma lição de gramática encontrada na planilha.")
            return {}
            
        # Preenche valores vazios
        gramatica_df = gramatica_df.fillna('')
        
        # Cria a estrutura de módulos
        modules = {}
        module_name = 'Gramática'  # Nome fixo já que estamos filtrando por isso
        modules[module_name] = []
        
        # Adiciona as lições
        for _, row in gramatica_df.iterrows():
            try:
                # Obtém a ordem, garantindo que seja um número inteiro
                try:
                    ordem = int(float(str(row['ordem']).strip() or '0'))
                except (ValueError, AttributeError):
                    ordem = 0
                    
                # Obtém o título, garantindo que seja uma string
                titulo = str(row['Título da Aula']).strip()
                if not titulo:
                    titulo = f"Lição {ordem}"
                    
                modules[module_name].append({
                    'title': titulo,
                    'video_url': str(row['Link do Vídeo']).strip(),
                    'doc_url': str(row['Link do Documento']).strip(),
                    'duration': str(row['Duração']).strip(),
                    'order': ordem
                })
                
            except Exception as e:
                st.warning(f"Erro ao processar linha da planilha: {str(e)}")
                continue
        
        # Ordena as lições pela ordem
        if module_name in modules:
            modules[module_name].sort(key=lambda x: x['order'])
            
        return modules
        
    except Exception as e:
        st.error(f"Erro ao carregar as lições: {str(e)}")
        import traceback
        st.error(traceback.format_exc())
        return {}
    except Exception as e:
        st.error(f"Erro ao carregar as lições: {str(e)}")
        return {}

# Aplicar estilos responsivos
from utils.module_utils import apply_responsive_styles
apply_responsive_styles()

# Conteúdo da página
st.markdown("""
## Aprenda a Gramática do Francês

Nesta seção, você encontrará vídeos e materiais sobre as regras gramaticais do francês.
""")

def display_grammar_lessons():
    modules = get_grammar_lessons()
    
    if not modules:
        st.warning("Nenhuma lição de gramática encontrada.")
        return
    
    for module_name, lessons in modules.items():
        st.markdown(f"## {module_name}")
        
        for lesson in lessons:
            with st.expander(f"📖 {lesson.get('title', 'Sem título')} ({lesson.get('duration', '')})", expanded=False):
                # Vídeo
                video_url = str(lesson.get('video_url', '')).strip()
                if video_url and video_url.lower() not in ['nan', 'none', '']:
                    st.markdown("### 🎥 Assista à Aula")
                    try:
                        file_id = video_url.split('/file/d/')[1].split('/')[0]
                        embed_url = f"https://drive.google.com/file/d/{file_id}/preview"
                        st.markdown(
                            f'<div style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; border-radius: 8px; margin: 20px 0;">'
                            f'<iframe src="{embed_url}" '
                            'style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: none;" '
                            'allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" '
                            'allowfullscreen></iframe>'
                            '</div>',
                            unsafe_allow_html=True
                        )
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

# Exibe as lições
display_grammar_lessons()
