import streamlit as st
import pandas as pd
from auth import auth_required
from utils.module_utils import get_module_lessons, display_page_header, apply_responsive_styles, display_progress_bar
from utils.excel_utils import load_excel_from_google_drive
from utils.progress_utils import save_progress, is_lesson_completed, get_module_progress

# Verifica autenticação
auth_required()

# Configuração da página
st.set_page_config(
    page_title="Gramática - Curso de Francês", 
    page_icon="📚",
    layout="wide"
)

# Constantes
SPREADSHEET_URL = "https://docs.google.com/spreadsheets/d/1RWd50uSh5AOTloRCXvIKPU9jBEUf4LI3/edit?usp=sharing"
MODULE_NAME = "gramatica"

# Aplicar estilos responsivos
apply_responsive_styles()

# Exibe o cabeçalho da página
display_page_header(
    module_name="gramática",
    icon="📚",
    description="Aprenda as regras e estruturas da língua francesa",
    total_lessons=0  # Será atualizado após carregar as lições
)

def get_grammar_lessons():
    """Busca as lições de gramática na planilha"""
    return get_module_lessons(SPREADSHEET_URL, "Gramática")

def display_grammar_lessons():
    """Exibe as lições de gramática"""
    # Carrega as lições do módulo
    module_data = get_grammar_lessons()
    
    if not module_data or 'lessons' not in module_data:
        st.warning("Nenhuma lição de gramática encontrada.")
        return
    
    lessons = module_data['lessons']
    module_id = "gramatica"
    
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
        
        # Cria um card para cada lição
        with st.expander(f"📚 {lesson.get('title', 'Sem título')} ({lesson.get('duration', '')})", 
                        expanded=is_completed):
            # Exibe o vídeo se houver
            video_url = str(lesson.get('video_url', '')).strip()
            if video_url and video_url.lower() not in ['nan', 'none', '']:
                st.markdown("### 🎥 Assista à Aula")
                try:
                    from utils.video_security import get_secure_video_embed
                    secure_embed = get_secure_video_embed(video_url)
                    st.markdown(secure_embed, unsafe_allow_html=True)
                except Exception as e:
                    st.warning(f"Não foi possível carregar o vídeo: {str(e)}")
            
            # Exibe o link do documento se houver
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
            
            # Exibe o link do YouTube se houver
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
            
            # Espaço no final da página
            st.markdown("""
            <div style="margin-bottom: 20px;"></div>
            """, unsafe_allow_html=True)
            
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
                    st.rerun()

# Exibe as lições
display_grammar_lessons()
