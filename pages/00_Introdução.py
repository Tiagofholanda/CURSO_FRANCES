import streamlit as st
from utils.excel_utils import load_excel_from_google_drive
import pandas as pd

# Configuração da página
st.set_page_config(
    page_title="Introdução - Curso de Francês", 
    page_icon="🇫🇷",
    layout="wide",
    initial_sidebar_state="expanded"
)

# URL da planilha do Google Sheets
SPREADSHEET_URL = "https://docs.google.com/spreadsheets/d/1RWd50uSh5AOTloRCXvIKPU9jBEUf4LI3/edit?usp=sharing"

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
try:
    from utils.video_security import get_secure_video_embed
    secure_embed = get_secure_video_embed(video_url)
    st.markdown(secure_embed, unsafe_allow_html=True)
except Exception as e:
    st.warning(f"Não foi possível carregar o vídeo de introdução: {str(e)}")

st.markdown("## 📂 Material de Apoio")
st.markdown("Faça o download do material complementar para acompanhar as aulas:")

st.markdown("""
<div style="margin: 20px 0;">
    <a href="https://drive.google.com/file/d/1RWd50uSh5AOTloRCXvIKPU9jBEUf4LI3/view?usp=sharing" target="_blank" style="display: inline-block; background-color: #4CAF50; color: white; padding: 10px 20px; text-align: center; text-decoration: none; border-radius: 5px; font-weight: bold;">
        📥 Baixar Material do Curso
    </a>
</div>
""", unsafe_allow_html=True)

st.markdown("## 📚 Conteúdo do Curso")

st.markdown("""
### 📌 Destaques:
- **Vocabulário**: Aprenda palavras e expressões essenciais
- **Pronúncia**: Melhore sua fala com exercícios práticos
- **Gramática**: Domine as estruturas da língua francesa

### 📅 Dicas de Estudo:
1. Estude regularmente, mesmo que por pouco tempo
2. Pratique a pronúncia em voz alta
3. Revise o conteúdo das aulas anteriores
4. Não tenha medo de errar - é parte do aprendizado!
""")

# Seção de Login (apenas para usuários não autenticados)
if 'authenticated' not in st.session_state or not st.session_state.authenticated:
    st.markdown("""
    <div style="text-align: center; margin: 30px 0;">
        <a href="/" target="_self" style="display: inline-block; background-color: #1E88E5; color: white; padding: 12px 24px; text-decoration: none; border-radius: 6px; font-weight: bold; font-size: 1.1em;">
            🔒 Fazer Login para Acessar Todo o Conteúdo
        </a>
    </div>
    """, unsafe_allow_html=True)
    
    # Adiciona um divisor visual
    st.markdown("<div style='margin: 40px 0; border-top: 1px solid #eee;'></div>", unsafe_allow_html=True)

# Seção de Conteúdo Principal
st.markdown("""
## 📅 Dicas de Estudo:
1. Estude regularmente, mesmo que por pouco tempo
2. Pratique a pronúncia em voz alta
3. Revise o conteúdo das aulas anteriores
4. Não tenha medo de errar - é parte do aprendizado!
""")

# Seção de Contato
st.markdown("---")
st.markdown("""
## 📱 Redes Sociais

Entre em contato pelo WhatsApp para obter suas credenciais de acesso ao curso de francês ou siga-nos no Instagram.
""")

# Container para os botões de contato
col1, col2 = st.columns(2)

with col1:
    st.markdown(
        '<a href="https://wa.me/5538998607764" target="_blank" style="display: inline-flex; align-items: center; justify-content: center; '
        'background-color: #25D366; color: white; padding: 10px 20px; border-radius: 6px; text-decoration: none; '
        'font-weight: 500; margin: 10px 0; width: 100%; text-align: center;">'
        '<img src="https://upload.wikimedia.org/wikipedia/commons/6/6b/WhatsApp.svg" width="24" style="margin-right: 10px;"> '
        'WhatsApp</a>',
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        '<a href="https://www.instagram.com/devgis_brasil/" target="_blank" style="display: inline-flex; align-items: center; justify-content: center; '
        'background: linear-gradient(45deg, #405DE6, #5851DB, #833AB4, #C13584, #E1306C, #FD1D1D); color: white; padding: 10px 20px; '
        'border-radius: 6px; text-decoration: none; font-weight: 500; margin: 10px 0; width: 100%; text-align: center;">'
        '<img src="https://upload.wikimedia.org/wikipedia/commons/e/e7/Instagram_logo_2016.svg" width="24" style="margin-right: 10px; filter: brightness(0) invert(1);"> '
        'Instagram</a>',
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
