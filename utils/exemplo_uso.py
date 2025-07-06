"""
Exemplo de uso das melhorias técnicas implementadas no Curso de Francês.

Este arquivo demonstra como utilizar as várias utilidades implementadas para melhorar
a performance, acessibilidade e responsividade do aplicativo.
"""
import streamlit as st
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

# Configuração da página
st.set_page_config(
    page_title="Exemplo de Uso - Curso de Francês",
    page_icon="🇫🇷",
    layout="wide"
)

# Inicializa as configurações de acessibilidade e responsividade
init_accessibility()
init_responsive()

# Adiciona link para pular para o conteúdo principal
add_skip_link()

# Título da página
st.title("Exemplo de Uso das Melhorias Técnicas")
st.markdown("---")

# Seção de exemplo de cache
st.header("1. Exemplo de Cache de Dados")

@cached_dataframe(ttl=3600)  # Cache por 1 hora
def load_data():
    """Função de exemplo que carrega dados com cache."""
    import pandas as pd
    import time
    
    # Simula um carregamento demorado
    time.sleep(2)
    
    # Retorna um DataFrame de exemplo
    return pd.DataFrame({
        'Palavra': ['Bonjour', 'Merci', 'Au revoir', 'S\'il vous plaît'],
        'Tradução': ['Olá', 'Obrigado', 'Adeus', 'Por favor'],
        'Categoria': ['Saudação', 'Agradecimento', 'Despedida', 'Cortesia']
    })

# Carrega os dados (usando cache)
with st.spinner('Carregando dados...'):
    df = load_data()

# Exibe os dados
st.dataframe(df)
st.info("🔍 Dica: Tente recarregar a página para ver o cache em ação!")

# Seção de exemplo de responsividade
st.header("2. Exemplo de Layout Responsivo")

# Cria colunas que se ajustam ao tamanho da tela
col1, col2 = responsive_columns([1, 1])

with col1:
    st.subheader("Coluna 1")
    st.write("Esta coluna se ajusta automaticamente ao tamanho da tela.")
    if is_mobile():
        st.info("📱 Você está acessando de um dispositivo móvel!")
    else:
        st.info("💻 Você está acessando de um desktop ou tablet!")

with col2:
    st.subheader("Coluna 2")
    st.write("Em telas pequenas, as colunas se empilham verticalmente.")
    st.image("https://via.placeholder.com/300x150?text=Imagem+Responsiva", 
             use_column_width=True)

# Seção de exemplo de vídeos
st.header("3. Exemplo de Player de Vídeo")

# Exemplo de vídeo incorporado
st.subheader("Vídeo incorporado")
display_video(
    "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    width=0,  # Largura responsiva
    height=0,  # Altura proporcional
    autoplay=False,
    controls=True,
    lazy=True
)

# Exemplo de card de vídeo
st.subheader("Card de Vídeo")
create_video_card(
    video_url="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    title="Aula de Francês - Introdução",
    description="Nesta aula, você aprenderá as saudações básicas em francês.",
    width=0,  # Largura responsiva
    show_thumbnail=True,
    show_title=True,
    show_description=True,
    show_controls=True
)

# Rodapé
st.markdown("---")
st.info("✨ Este é um exemplo das melhorias técnicas implementadas no Curso de Francês.")

# Adiciona um botão para limpar o cache (apenas para demonstração)
if st.button("🔄 Limpar Cache"):
    from utils import clear_cache
    if clear_cache():
        st.success("✅ Cache limpo com sucesso!")
        st.rerun()
    else:
        st.error("❌ Erro ao limpar o cache.")
