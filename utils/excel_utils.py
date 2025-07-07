import pandas as pd
import streamlit as st
import requests
from urllib.parse import urlparse, parse_qs
from io import BytesIO
import time

def get_google_sheets_url(url):
    """
    Converte a URL de edição para URL de exportação CSV
    
    Args:
        url: URL da planilha do Google Sheets
        
    Returns:
        URL de exportação no formato XLSX
    """
    if not url or not isinstance(url, str):
        st.error("URL inválida ou não fornecida")
        return None
    
    try:
        # Remove parâmetros de consulta se existirem
        clean_url = url.split('?')[0]
        
        # Verifica se é uma URL do Google Sheets
        if 'docs.google.com/spreadsheets/d/' in clean_url:
            # Extrai o ID da planilha da URL
            if '/d/' in clean_url and ('/edit' in clean_url or '/view' in clean_url):
                file_id = clean_url.split('/d/')[1].split('/')[0]
            elif 'id=' in clean_url:
                file_id = clean_url.split('id=')[1].split('&')[0]
            else:
                st.error("Formato de URL do Google Sheets não reconhecido")
                return None
            
            # Retorna a URL de exportação
            export_url = f"https://docs.google.com/spreadsheets/d/{file_id}/export?format=xlsx"
            return export_url
            
        return url
    except Exception as e:
        st.error(f"Erro ao processar a URL da planilha: {str(e)}")
        st.error(f"URL fornecida: {url}")
        return None

def load_excel_from_google_drive(url, max_retries=3, retry_delay=2):
    """
    Carrega um arquivo Excel do Google Drive com tratamento de erros e retentativas
    
    Args:
        url: URL da planilha do Google Sheets
        max_retries: Número máximo de tentativas em caso de falha
        retry_delay: Atraso entre as tentativas em segundos
        
    Returns:
        DataFrame com os dados da planilha ou DataFrame vazio em caso de erro
    """
    # Inicializa a sessão de debug se não existir
    if 'debug_info' not in st.session_state:
        st.session_state.debug_info = []
    
    def add_debug_info(message):
        """Adiciona uma mensagem ao log de depuração"""
        timestamp = pd.Timestamp.now().strftime('%H:%M:%S')
        st.session_state.debug_info.append(f"[{timestamp}] {message}")
    
    add_debug_info(f"Iniciando carregamento da planilha: {url}")
    
    if not url:
        error_msg = "URL da planilha não fornecida."
        add_debug_info(error_msg)
        st.error(error_msg)
        return pd.DataFrame()
    
    # Verifica se a URL é uma URL do Google Sheets
    if 'docs.google.com/spreadsheets/' not in url:
        error_msg = "URL inválida. Por favor, forneça uma URL do Google Sheets."
        add_debug_info(error_msg)
        st.error(error_msg)
        return pd.DataFrame()
    
    # Tenta converter a URL para o formato de exportação
    add_debug_info("Convertendo URL para formato de exportação...")
    export_url = get_google_sheets_url(url)
    
    if not export_url:
        error_msg = "Não foi possível converter a URL para o formato de exportação."
        add_debug_info(error_msg)
        st.error(error_msg)
        return pd.DataFrame()
    
    add_debug_info(f"URL de exportação gerada: {export_url}")
    
    # Tenta baixar o arquivo com várias tentativas
    for attempt in range(max_retries):
        try:
            add_debug_info(f"Tentativa {attempt + 1} de {max_retries} - Baixando planilha...")
            
            # Configura o cabeçalho para simular um navegador
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            # Baixa o arquivo
            response = requests.get(export_url, headers=headers, timeout=30)
            response.raise_for_status()
            
            add_debug_info("Planilha baixada com sucesso. Processando dados...")
            
            # Carrega o conteúdo no pandas
            df = pd.read_excel(BytesIO(response.content))
            
            # Verifica se o DataFrame está vazio
            if df.empty:
                add_debug_info("Aviso: O DataFrame retornado está vazio.")
            else:
                add_debug_info(f"Planilha carregada com sucesso. Dimensões: {df.shape}")
                add_debug_info(f"Colunas encontradas: {', '.join(df.columns)}")
            
            return df
            
        except requests.exceptions.RequestException as e:
            if attempt == max_retries - 1:
                st.error(f"Erro ao acessar a planilha após {max_retries} tentativas.")
                return pd.DataFrame()
            time.sleep(retry_delay)
            
        except Exception as e:
            st.error("Erro ao processar a planilha.")
            return pd.DataFrame()
    
    return pd.DataFrame()

def display_videos(df, video_column='Link do Vídeo', title_column='Título da Aula', module_column='Módulo', duration_column='Duração', doc_column='Link do Documento'):
    """
    Exibe vídeos a partir de um DataFrame com as colunas específicas da planilha
    """
    if df.empty:
        st.warning("Nenhum vídeo encontrado na planilha.")
        return
    
    # Ordena por módulo e ordem, se existirem as colunas
    if 'Módulo' in df.columns and 'ordem' in df.columns:
        df = df.sort_values(by=['Módulo', 'ordem'])
    
    current_module = None
    
    for _, row in df.iterrows():
        video_url = row.get(video_column, '')
        if not video_url or pd.isna(video_url):
            continue
            
        # Limpa a URL se necessário
        video_url = str(video_url).strip()
        
        # Verifica se é um novo módulo
        if module_column in row and not pd.isna(row[module_column]):
            module_name = str(row[module_column])
            if module_name != current_module:
                current_module = module_name
                st.markdown(f"## Módulo: {current_module}")
        
        # Cria um container para cada vídeo
        with st.container():
            st.markdown("---")
            
            # Exibe o título se disponível
            if title_column in row and not pd.isna(row[title_column]):
                st.subheader(str(row[title_column]))
            
            # Exibe a duração se disponível
            if duration_column in row and not pd.isna(row[duration_column]):
                st.caption(f"⏱️ {row[duration_column]}")
            
            # Exibe o vídeo
            try:
                st.video(video_url)
            except Exception as e:
                st.error(f"Erro ao carregar o vídeo: {video_url}")
                st.write(f"Link do vídeo: [{video_url}]({video_url})")
            
            # Exibe link do documento se disponível
            if doc_column in row and not pd.isna(row[doc_column]):
                doc_url = str(row[doc_column]).strip()
                if doc_url and doc_url.lower() not in ['nan', 'none', '']:
                    st.markdown(f"📄 [Abrir documento]({doc_url})")
            
            st.markdown("\n")
