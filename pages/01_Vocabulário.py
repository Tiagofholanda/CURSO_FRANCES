import streamlit as st
import pandas as pd
from auth import auth_required
from utils.module_utils import get_module_lessons, display_progress_bar, display_lesson, apply_responsive_styles

# Verifica autenticação
auth_required()

# Configuração da página
st.set_page_config(
    page_title="Vocabulário - Curso de Francês", 
    page_icon="📚",
    layout="wide"
)

# Aplica estilos responsivos
apply_responsive_styles()

# URL da planilha
SPREADSHEET_URL = "https://docs.google.com/spreadsheets/d/1RWd50uSh5AOTloRCXvIKPU9jBEUf4LI3/edit?usp=sharing"
MODULE_NAME = "Vocabulário"

# Cabeçalho
st.markdown(f"""
<div class="header">
    <h1>📚 {MODULE_NAME} Francês</h1>
    <p>Aprenda novas palavras e expressões em francês</p>
</div>
""", unsafe_allow_html=True)

def get_vocabulary_lessons():
    """Busca as lições de vocabulário na planilha"""
    return get_module_lessons(SPREADSHEET_URL, MODULE_NAME)

def display_vocabulary_lessons():
    """Exibe as lições de vocabulário"""
    # Carrega as lições do módulo
    module_data = get_vocabulary_lessons()
    
    if not module_data or 'lessons' not in module_data:
        st.warning("Nenhuma lição de vocabulário encontrada.")
        return
    
    lessons = module_data['lessons']
    
    # Exibe a barra de progresso
    display_progress_bar(MODULE_NAME.lower(), len(lessons))
    
    # Exibe as lições
    st.markdown("## 📋 Lições Disponíveis")
    
    for lesson in lessons:
        display_lesson(lesson, MODULE_NAME.lower())

# Exibe as lições
display_vocabulary_lessons()
