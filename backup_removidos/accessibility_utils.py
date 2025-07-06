import streamlit as st
from typing import Dict, Any

def apply_accessibility_settings():
    """Aplica as configurações de acessibilidade."""
    # Adiciona teclas de atalho
    st.markdown("""
    <script>
    document.addEventListener('keydown', function(e) {
        // Alt+1: Ir para o conteúdo principal
        if (e.altKey && e.key === '1') {
            document.querySelector('main').focus();
        }
        // Alt+2: Ir para a navegação
        else if (e.altKey && e.key === '2') {
            document.querySelector('header').focus();
        }
        // Alt+0: Mostrar ajuda de teclas de atalho
        else if (e.altKey && e.key === '0') {
            alert('Teclas de atalho disponíveis:\\n\\n' +
                  'Alt+1: Ir para o conteúdo principal\\n' +
                  'Alt+2: Ir para a navegação\\n' +
                  'Alt+0: Mostrar esta ajuda');
        }
    });
    </script>
    """, unsafe_allow_html=True)
    
    # Adiciona ARIA labels para elementos importantes
    st.markdown("""
    <style>
    /* Melhora o contraste */
    body {
        --primary-color: #1E88E5;
        --primary-dark: #1565C0;
        --text-color: #333333;
        --background-color: #FFFFFF;
        --secondary-background: #F5F5F5;
    }
    
    /* Melhora o foco para navegação por teclado */
    :focus {
        outline: 3px solid var(--primary-color) !important;
        outline-offset: 2px;
    }
    
    /* Ajustes de contraste */
    .stButton > button:first-child {
        background-color: var(--primary-color);
        color: white;
    }
    
    .stButton > button:first-child:hover {
        background-color: var(--primary-dark);
    }
    
    /* Melhora a legibilidade */
    body, .stTextInput > div > div > input {
        color: var(--text-color);
    }
    
    /* Classes para alto contraste */
    .high-contrast {
        --primary-color: #000000;
        --primary-dark: #000000;
        --text-color: #000000;
        --background-color: #FFFFFF;
        --secondary-background: #EEEEEE;
    }
    
    /* Classes para modo escuro */
    .dark-mode {
        --primary-color: #90CAF9;
        --primary-dark: #64B5F6;
        --text-color: #E0E0E0;
        --background-color: #121212;
        --secondary-background: #1E1E1E;
    }
    </style>
    """, unsafe_allow_html=True)

def add_skip_link():
    """Adiciona um link de pular para o conteúdo principal."""
    st.markdown("""
    <a href="#main-content" class="skip-link">Pular para o conteúdo principal</a>
    <style>
    .skip-link {
        position: absolute;
        top: -40px;
        left: 0;
        background: #000;
        color: white;
        padding: 8px;
        z-index: 100;
        transition: top 0.3s;
    }
    .skip-link:focus {
        top: 0;
    }
    </style>
    """, unsafe_allow_html=True)

def add_aria_labels(elements: Dict[str, str]):
    """
    Adiciona atributos ARIA a elementos da página.
    
    Args:
        elements: Dicionário onde a chave é o seletor CSS e o valor é o texto ARIA
    """
    if not elements:
        return
        
    aria_script = "<script>"
    for selector, label in elements.items():
        aria_script += f"""
        document.querySelectorAll('{selector}').forEach(el => {{
            el.setAttribute('aria-label', '{label}');
        }});
        """
    aria_script += "</script>"
    
    st.markdown(aria_script, unsafe_allow_html=True)

def init_accessibility():
    """Inicializa todas as configurações de acessibilidade."""
    apply_accessibility_settings()
    add_skip_link()
    
    # Adiciona botão de alto contraste
    if st.sidebar.button("🔍 Alto Contraste"):
        st.session_state.high_contrast = not st.session_state.get('high_contrast', False)
    
    # Aplica o tema de alto contraste se ativado
    if st.session_state.get('high_contrast', False):
        st.markdown('<div class="high-contrast">', unsafe_allow_html=True)
        
    # Adiciona botão de modo escuro
    if st.sidebar.button("🌙 Modo Escuro"):
        st.session_state.dark_mode = not st.session_state.get('dark_mode', False)
    
    # Aplica o modo escuro se ativado
    if st.session_state.get('dark_mode', False):
        st.markdown('<div class="dark-mode">', unsafe_allow_html=True)
