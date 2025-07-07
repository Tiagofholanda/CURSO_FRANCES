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

# URL da planilha do Google Sheets
SPREADSHEET_URL = "https://docs.google.com/spreadsheets/d/1RWd50uSh5AOTloRCXvIKPU9jBEUf4LI3/edit?usp=sharing"

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

# Carrega os dados da planilha
try:
    df = load_excel_from_google_drive(SPREADSHEET_URL)
    if df.empty:
        st.error("Não foi possível carregar a planilha. Por favor, tente novamente mais tarde.")
        st.stop()
except Exception as e:
    st.error("Erro ao carregar o conteúdo. Por favor, tente novamente mais tarde.")
    st.stop()

# Carrega os dados dos módulos
modules_data = get_modules_data(SPREADSHEET_URL)

# Barra lateral para navegação
st.sidebar.title("Navegação")

# Lista de módulos para seleção
selected_module = st.sidebar.selectbox(
    "Selecione o Módulo",
    list(modules_data.keys()) if modules_data else ["Nenhum módulo disponível"]
)

# Se não houver módulos, mostra mensagem
if not modules_data:
    st.error("Nenhum módulo encontrado na planilha.")
    st.stop()

# Exibe o conteúdo do módulo selecionado
st.title(f"Módulo: {selected_module}")

# Exibe as aulas do módulo
for lesson in modules_data[selected_module]:
    with st.expander(f" {lesson['title']} ({lesson.get('duration', '')})", expanded=False):
        # Mostra o vídeo incorporado com medidas de segurança
        video_url = str(lesson['video_url']).strip()
        if video_url and video_url.lower() not in ['nan', 'none', '']:
            st.markdown("### Assista à Aula")
            try:
                from utils.video_security import get_secure_video_embed
                secure_embed = get_secure_video_embed(video_url)
                st.markdown(secure_embed, unsafe_allow_html=True)
            except Exception as e:
                st.warning(f"Não foi possível carregar o vídeo: {str(e)}")
        else:
            st.warning("Link de vídeo não disponível.")
        
        # Mostra o link para baixar o documento, se disponível
        doc_url = str(lesson.get('doc_url', '')).strip()
        if doc_url and doc_url.lower() not in ['nan', 'none', '']:
            st.markdown("## Material de Apoio")
            
            if 'drive.google.com' in doc_url and '/file/d/' in doc_url:
                file_id = doc_url.split('/file/d/')[1].split('/')[0]
                # Mostra o documento em um iframe
                st.markdown(
                    f'<div style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; border-radius: 8px; margin: 20px 0; border: 1px solid #e0e0e0;">'
                    f'<iframe src="https://drive.google.com/file/d/{file_id}/preview" '
                    'style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: none;" '
                    'allow="autoplay"></iframe>'
                    '</div>',
                    unsafe_allow_html=True
                )
                
                # Botão para baixar o documento
                download_url = f"https://drive.google.com/uc?export=download&id={file_id}"
                st.markdown(
                    f'<a href="{download_url}" '
                    'style="display: inline-flex; align-items: center; background-color: #1E88E5; color: white; '
                    'padding: 10px 20px; border-radius: 4px; text-decoration: none; font-weight: bold; margin: 10px 0;" '
                    'target="_blank">'
                    '📄 Baixar Documento</a>',
                    unsafe_allow_html=True
                )
            else:
                # Se não for um link do Google Drive, mostra apenas o link
                st.markdown(
                    f'<a href="{doc_url}" target="_blank">Abrir documento</a>',
                    unsafe_allow_html=True
                )

# Espaço no final da página
st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)
