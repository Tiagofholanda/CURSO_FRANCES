import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from typing import Dict, List, Optional
import streamlit as st

def get_google_sheet_data(credentials_file: str, spreadsheet_url: str, worksheet_name: str = None) -> pd.DataFrame:
    """
    Lê dados de uma planilha do Google Sheets.
    
    Args:
        credentials_file: Caminho para o arquivo de credenciais JSON
        spreadsheet_url: URL da planilha do Google Sheets
        worksheet_name: Nome da planilha específica (opcional)
        
    Returns:
        DataFrame do pandas com os dados da planilha
    """
    try:
        # Configura as permissões
        scope = ['https://spreadsheets.google.com/feeds',
                'https://www.googleapis.com/auth/drive']
        
        # Autentica
        creds = ServiceAccountCredentials.from_json_keyfile_name(credentials_file, scope)
        client = gspread.authorize(creds)
        
        # Abre a planilha
        spreadsheet = client.open_by_url(spreadsheet_url)
        
        # Seleciona a planilha específica se fornecida
        if worksheet_name:
            worksheet = spreadsheet.worksheet(worksheet_name)
        else:
            worksheet = spreadsheet.sheet1
        
        # Converte para DataFrame
        data = worksheet.get_all_records()
        df = pd.DataFrame(data)
        
        return df
    except Exception as e:
        st.error(f"Erro ao acessar o Google Sheets: {str(e)}")
        return pd.DataFrame()

def display_videos_from_dataframe(df: pd.DataFrame, video_column: str, title_column: str = None, 
                               description_column: str = None) -> None:
    """
    Exibe vídeos a partir de um DataFrame.
    
    Args:
        df: DataFrame contendo os dados
        video_column: Nome da coluna com as URLs dos vídeos
        title_column: Nome da coluna com os títulos (opcional)
        description_column: Nome da coluna com as descrições (opcional)
    """
    if df.empty:
        st.warning("Nenhum dado encontrado para exibir.")
        return
    
    for idx, row in df.iterrows():
        video_url = row.get(video_column, '')
        if not video_url:
            continue
            
        # Cria um container para cada vídeo
        with st.container():
            st.markdown("---")
            
            # Exibe o título se disponível
            if title_column and title_column in row:
                st.subheader(row[title_column])
            
            # Exibe o vídeo
            st.video(video_url)
            
            # Exibe a descrição se disponível
            if description_column and description_column in row:
                st.write(row[description_column])
            
            st.markdown("\n")
