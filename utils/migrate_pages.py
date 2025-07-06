"""
Script para migrar as páginas existentes para usar as novas melhorias técnicas.

Este script ajuda a atualizar as páginas existentes para usar as novas funcionalidades
de cache, carregamento preguiçoso, acessibilidade e responsividade.
"""
import os
import re
from pathlib import Path

# Diretório das páginas
PAGES_DIR = os.path.join(os.path.dirname(__file__), 'pages')

# Lista de arquivos para migrar
PAGE_FILES = [
    '00_Introdução.py',
    '01_Vocabulário.py',
    '02_Pronúncia.py',
    '03_Gramática.py'
]

# Cabeçalho comum para as páginas
COMMON_HEADER = """"""
# Importações padrão
import streamlit as st
import pandas as pd
from utils import (
    # Acessibilidade
    init_accessibility,
    add_skip_link,
    
    # Performance
    cached_dataframe,
    
    # Responsividade
    init_responsive,
    responsive_columns,
    is_mobile,
    
    # Vídeos
    display_video,
    create_video_card
)

# Inicializa as configurações de acessibilidade e responsividade
init_accessibility()
init_responsive()

# Adiciona link para pular para o conteúdo principal
add_skip_link()

# Configuração da página
st.set_page_config(
    page_title="Curso de Francês",
    page_icon="🇫🇷",
    layout="wide"
)

# Adicione o CSS personalizado
def load_css():
    """Carrega o CSS personalizado."""
    st.markdown("""
    <style>
        /* Estilos personalizados aqui */
        .main .block-container {
            max-width: 1200px;
        }
        
        /* Melhora o contraste para acessibilidade */
        :root {
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
    </style>
    """, unsafe_allow_html=True)

# Carrega o CSS
load_css()
""""

def migrate_file(file_path):
    """Migra um arquivo de página para usar as novas melhorias."""
    print(f"Migrando {file_path}...")
    
    # Lê o conteúdo atual do arquivo
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Verifica se o arquivo já foi migrado
    if 'from utils import' in content and 'init_accessibility' in content:
        print(f"  ✅ {os.path.basename(file_path)} já foi migrado.")
        return False
    
    # Adiciona o cabeçalho comum
    new_content = COMMON_HEADER + '\n\n' + content
    
    # Substitui st.video por display_video
    new_content = re.sub(
        r'st\.video\(([^)]+)\)',
        r'display_video(\1)',
        new_content
    )
    
    # Adiciona suporte a cache para funções que carregam dados
    if 'load_data' in new_content and '@cached_dataframe' not in new_content:
        new_content = re.sub(
            r'def load_data\(',
            r'@cached_dataframe(ttl=3600)  # Cache por 1 hora\ndef load_data(',
            new_content
        )
    
    # Salva o arquivo migrado
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"  ✅ {os.path.basename(file_path)} migrado com sucesso!")
    return True

def main():
    """Função principal."""
    print("Iniciando migração das páginas...\n")
    
    # Cria o diretório de páginas se não existir
    os.makedirs(PAGES_DIR, exist_ok=True)
    
    # Migra cada arquivo de página
    migrated_count = 0
    for page_file in PAGE_FILES:
        file_path = os.path.join(PAGES_DIR, page_file)
        if os.path.exists(file_path):
            if migrate_file(file_path):
                migrated_count += 1
        else:
            print(f"  ⚠️ {page_file} não encontrado.")
    
    print(f"\nMigração concluída! {migrated_count} arquivos foram migrados.")

if __name__ == "__main__":
    main()
