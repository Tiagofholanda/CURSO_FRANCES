"""
Configurações de segurança para o aplicativo Streamlit.
"""
import streamlit as st

def set_security_headers():
    """
    Configura os cabeçalhos de segurança HTTP, incluindo Content Security Policy (CSP).
    """
    # Configura a CSP para permitir iframes do Google Drive
    csp = """
    default-src 'self';
    script-src 'self' 'unsafe-inline' 'unsafe-eval' https://cdn.jsdelivr.net;
    style-src 'self' 'unsafe-inline' https://fonts.googleapis.com;
    img-src 'self' data: https://*.google.com https://*.googleusercontent.com;
    font-src 'self' https://fonts.gstatic.com;
    frame-src 'self' https://drive.google.com https://www.youtube.com https://www.youtube-nocookie.com;
    connect-src 'self' https://*.google.com https://*.googleapis.com;
    media-src 'self' https://*.google.com;
    """
    
    # Configura o Streamlit para usar os cabeçalhos personalizados
    st.set_page_config(
        page_title="Aulas de Francês",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Adiciona meta tags de segurança no cabeçalho HTML
    st.markdown(
        f"""
        <meta http-equiv="Content-Security-Policy" content="{csp.replace('\n', ' ').strip()}">
        <meta http-equiv="X-Content-Type-Options" content="nosniff">
        <meta http-equiv="X-Frame-Options" content="SAMEORIGIN">
        <meta http-equiv="X-XSS-Protection" content="1; mode=block">
        <meta name="referrer" content="strict-origin-when-cross-origin">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        """,
        unsafe_allow_html=True
    )
