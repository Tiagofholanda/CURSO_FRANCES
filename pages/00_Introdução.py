import streamlit as st
from auth import login, auth_required, logout

# Configuração da página
st.set_page_config(
    page_title="Introdução - Curso de Francês", 
    page_icon="🇫🇷",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Verifica se já está autenticado
if 'authenticated' in st.session_state and st.session_state.authenticated:
    st.switch_page("pages/01_Vocabulário.py")
    st.stop()

def get_embed_url(video_url):
    """Converte URL do Google Drive para URL de incorporação"""
    try:
        file_id = video_url.split('/file/d/')[1].split('/')[0]
        return f"https://drive.google.com/file/d/{file_id}/preview"
    except:
        return None

def get_download_url(drive_url):
    """Converte URL do Google Drive para URL de download direto"""
    try:
        file_id = drive_url.split('/file/d/')[1].split('/')[0]
        return f"https://drive.google.com/uc?export=download&id={file_id}"
    except:
        return None

# Título da página
st.markdown("""
<div style="text-align: center; margin-bottom: 30px;">
    <h1 style="color: #2c3e50; margin-bottom: 10px;">Bem-vindo ao Curso de Francês! 🇫🇷</h1>
    <p style="color: #7f8c8d; font-size: 1.1em;">Aprenda francês de forma simples e eficiente</p>
</div>
""", unsafe_allow_html=True)

# Conteúdo da introdução
st.markdown("""
## 🔍 Sobre o Curso

Este é um curso completo de francês desenvolvido para ajudar você a aprender o idioma de forma prática e eficiente. 

### 📚 O que você vai aprender:
- Vocabulário essencial para o dia a dia
- Pronúncia correta das palavras
- Estruturas gramaticais importantes
- Expressões úteis para viagens

### 🎯 Como começar:
1. Faça login para acessar o conteúdo completo
2. Navegue pelas lições no menu lateral
3. Pratique regularmente para melhorar seu francês

## 🎥 Vídeo de Introdução
""")

# Vídeo incorporado
video_url = "https://drive.google.com/file/d/174Q2EThuNIFj8bn0lKCiZQBvBRDzZLcB/view"
embed_url = get_embed_url(video_url)

if embed_url:
    st.markdown(
        f'<div style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; border-radius: 8px; margin: 20px 0;">'
        f'<iframe src="{embed_url}" '
        'style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: none;" '
        'allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" '
        'allowfullscreen></iframe>'
        '</div>',
        unsafe_allow_html=True
    )

st.markdown("## 📂 Material de Apoio")
st.markdown("Faça o download do material complementar para acompanhar as aulas:")

st.markdown("""
<div style="margin: 20px 0;">
    <a href="https://drive.google.com/file/d/1RWd50uSh5AOTloRCXvIKPU9jBEUf4LI3/view?usp=sharing" target="_blank" style="display: inline-block; background-color: #4CAF50; color: white; padding: 10px 20px; text-align: center; text-decoration: none; border-radius: 5px; font-weight: bold;">
        📥 Baixar Material do Curso
    </a>
</div>
""", unsafe_allow_html=True)

st.markdown("## 🔒 Acesso às Aulas")
st.markdown("Para acessar todo o conteúdo do curso, faça login com suas credenciais:")

# Seção de login
st.markdown("### Faça login para continuar")
login()

# Rodapé
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #7f8c8d; margin-top: 50px;">
    <p>Curso de Francês &copy; 2023 - Todos os direitos reservados</p>
    <p style="font-size: 0.8em;">Desenvolvido com ❤️ para amantes da língua francesa</p>
</div>
""", unsafe_allow_html=True)

doc_url = "https://drive.google.com/file/d/1bZSa8HZrrT1zzjkLhXwGq-UrKLDglkSr/view"
download_url = get_download_url(doc_url)

if download_url:
    st.markdown(
        f'<a href="{download_url}" '
        'style="display: inline-flex; align-items: center; background-color: #1E88E5; color: white; '
        'padding: 10px 20px; border-radius: 4px; text-decoration: none; font-weight: bold; margin: 10px 0;" '
        'target="_blank">'
        '📄 Baixar Material de Apoio</a>',
        unsafe_allow_html=True
    )

# Estilos adicionais para o botão de login
st.markdown("""
<style>
    .stButton>button {
        display: block;
        margin: 20px auto;
        background-color: #1E88E5;
        color: white;
        font-weight: bold;
        padding: 12px 32px;
        border-radius: 8px;
        border: none;
        font-size: 1.1em;
        transition: background-color 0.3s;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #1565C0;
    }
    h2, h3 {
        color: #1E88E5;
        margin-top: 30px;
    }
    .login-container {
        max-width: 500px;
        margin: 0 auto;
    }
</style>
""", unsafe_allow_html=True)
