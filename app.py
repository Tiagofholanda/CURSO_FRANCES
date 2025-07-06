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

# Configuração da página
st.set_page_config(page_title="Aulas de Francês", layout="wide")

# Inicializa a sessão se não existir
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.username = ''
    st.session_state.role = ''
    # Redireciona para a página de introdução se não estiver autenticado
    st.switch_page("pages/00_Introdução.py")

def get_direct_video_url(drive_url):
    """
    Obtém a URL direta para incorporação do vídeo do Google Drive
    com tela cheia habilitada diretamente no iframe
    """
    try:
        if not drive_url or pd.isna(drive_url):
            return None
            
        drive_url = str(drive_url).strip()
        
        # Extrai o ID do arquivo de diferentes formatos de URL
        if 'drive.google.com' in drive_url:
            if '/file/d/' in drive_url:
                file_id = drive_url.split('/file/d/')[1].split('/')[0]
            elif 'id=' in drive_url:
                file_id = drive_url.split('id=')[1].split('&')[0]
            else:
                return None
                
            # Retorna a URL formatada para visualização direta em tela cheia
            return f"https://drive.google.com/file/d/{file_id}/preview?autoplay=1&mute=0&controls=1&showinfo=0&modestbranding=1&fs=1"
            
        return drive_url
    except Exception as e:
        st.error(f"Erro ao processar URL do vídeo: {str(e)}")
        return None

# URL da planilha do Google Sheets
SPREADSHEET_URL = "https://docs.google.com/spreadsheets/d/1RWd50uSh5AOTloRCXvIKPU9jBEUf4LI3/edit?usp=sharing"

# Se não estiver autenticado, redireciona para a introdução
if not st.session_state.authenticated:
    st.switch_page("pages/00_Introdução.py")
    st.stop()

# Se chegou até aqui, o usuário está autenticado

# Barra lateral com menu de navegação
st.sidebar.title(f"Olá, {st.session_state.username}")

# Menu de navegação
st.sidebar.markdown("### Navegação")
page = st.sidebar.radio(
    "Selecione uma seção:",
    ["Módulos do Curso", "Vocabulário", "Pronúncia", "Gramática"]
)

# Navegação entre páginas
if page == "Vocabulário":
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
        # Mostra o vídeo incorporado
        video_url = str(lesson['video_url']).strip()
        if video_url and video_url.lower() not in ['nan', 'none', '']:
            # Obtém a URL para incorporação do vídeo
            embed_url = get_direct_video_url(video_url)
            
            if embed_url:
                # Adiciona um ID único para o container do vídeo
                video_id = f"video-{lesson['title'].replace(' ', '-').lower()}"
                
                # Exibe o vídeo em um iframe
                st.markdown("### Assista à Aula")
                st.markdown(
                    f'<div style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; border-radius: 8px; margin: 20px 0;">'
                    f'<iframe src="{embed_url}" '
                    'style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: none;" '
                    'allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" '
                    'allowfullscreen></iframe>'
                    '</div>',
                    unsafe_allow_html=True
                )
                
                # Remove o código JavaScript antigo que não é mais necessário
                pass
                
            else:
                st.warning("Não foi possível carregar o vídeo. Verifique o link.")
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

# Rodapé
st.markdown("---")
col1, col2 = st.columns([3, 1])
with col1:
    st.markdown("Desenvolvido para estudantes de francês")
with col2:
    st.markdown(
        '<a href="https://wa.me/5538998607764" target="_blank" style="display: inline-flex; align-items: center; '
        'background-color: #25D366; color: white; padding: 8px 16px; border-radius: 4px; text-decoration: none; '
        'font-weight: 500;">'
        '<img src="https://upload.wikimedia.org/wikipedia/commons/6/6b/WhatsApp.svg" width="20" style="margin-right: 8px;"> '
        'Fale pelo WhatsApp</a>',
        unsafe_allow_html=True
    )
