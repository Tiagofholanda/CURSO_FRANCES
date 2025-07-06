"""
Configurações de segurança para o aplicativo Streamlit.
"""
import streamlit as st
from streamlit.web.server.websocket_headers import _get_websocket_headers

def set_security_headers():
    """
    Configura os cabeçalhos de segurança HTTP, incluindo Content Security Policy (CSP).
    """
    # Obtém os cabeçalhos da requisição WebSocket
    headers = _get_websocket_headers()
    
    if headers is None:
        headers = {}
    
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
    
    # Adiciona os cabeçalhos de segurança
    headers['Content-Security-Policy'] = csp.replace('\n', ' ').strip()
    headers['X-Content-Type-Options'] = 'nosniff'
    headers['X-Frame-Options'] = 'SAMEORIGIN'
    headers['X-XSS-Protection'] = '1; mode=block'
    
    # Configura o Streamlit para usar os cabeçalhos personalizados
    st.set_page_config(
        page_title="Aulas de Francês",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Adiciona meta tags de segurança no cabeçalho HTML
    st.markdown(
        """
        <meta http-equiv="Content-Security-Policy" content="default-src 'self'; 
            script-src 'self' 'unsafe-inline' 'unsafe-eval' https://cdn.jsdelivr.net;
            style-src 'self' 'unsafe-inline' https://fonts.googleapis.com;
            img-src 'self' data: https://*.google.com https://*.googleusercontent.com;
            font-src 'self' https://fonts.gstatic.com;
            frame-src 'self' https://drive.google.com https://www.youtube.com https://www.youtube-nocookie.com;
            connect-src 'self' https://*.google.com https://*.googleapis.com;
            media-src 'self' https://*.google.com;">
        <meta http-equiv="X-Content-Type-Options" content="nosniff">
        <meta http-equiv="X-Frame-Options" content="SAMEORIGIN">
        <meta http-equiv="X-XSS-Protection" content="1; mode=block">
        """,
        unsafe_allow_html=True
    )
