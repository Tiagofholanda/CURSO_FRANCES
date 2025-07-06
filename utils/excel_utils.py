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
        return None
        
    try:
        if 'docs.google.com/spreadsheets/d/' in url:
            # Extrai o ID da planilha da URL
            if '/edit' in url:
                file_id = url.split('/d/')[1].split('/edit')[0]
            else:
                file_id = url.split('/d/')[1].split('/')[0].split('?')[0]
                
            return f"https://docs.google.com/spreadsheets/d/{file_id}/export?format=xlsx"
        return url
    except Exception as e:
        st.error(f"Erro ao processar a URL da planilha: {str(e)}")
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
    if not url:
        st.error("URL da planilha não fornecida.")
        return pd.DataFrame()
        
    export_url = get_google_sheets_url(url)
    if not export_url:
        return pd.DataFrame()
        
    for attempt in range(max_retries):
        try:
            # Faz o download do arquivo
            response = requests.get(export_url, timeout=30)
            response.raise_for_status()
            
            # Carrega o arquivo Excel
            df = pd.read_excel(BytesIO(response.content))
            
            # Verifica se o DataFrame está vazio
            if df.empty:
                st.warning("A planilha está vazia.")
                return df
                
            # Verifica se as colunas necessárias existem
            required_columns = ['Módulo', 'Título da Aula', 'Link do Vídeo', 'Link do Documento', 'Duração', 'ordem']
            missing_columns = [col for col in required_columns if col not in df.columns]
            
            if missing_columns:
                st.warning(f"Atenção: Algumas colunas esperadas não foram encontradas: {', '.join(missing_columns)}")
            
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
