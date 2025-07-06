import streamlit as st
from typing import Dict, List, Optional, Tuple, Union
import base64

def apply_responsive_styles():
    """Aplica estilos CSS para melhorar a responsividade."""
    st.markdown("""
    <style>
    /* Estilos base responsivos */
    .main .block-container {
        max-width: 1200px;
        padding: 1rem 1.5rem;
    }
    
    /* Ajustes para telas médias (tablets) */
    @media (max-width: 992px) {
        .main .block-container {
            padding: 0.75rem 1rem;
        }
        
        /* Ajusta o tamanho da fonte para melhor legibilidade */
        body {
            font-size: 15px;
        }
        
        /* Ajusta o padding dos expanders */
        .streamlit-expanderHeader {
            padding: 0.75rem 1rem;
        }
    }
    
    /* Ajustes para telas pequenas (smartphones) */
    @media (max-width: 768px) {
        .main .block-container {
            padding: 0.5rem 0.75rem;
        }
        
        /* Ajusta o tamanho da fonte */
        body {
            font-size: 14px;
        }
        
        /* Melhora o espaçamento dos elementos */
        .stButton > button {
            width: 100%;
            margin: 0.25rem 0;
        }
        
        /* Ajusta o layout das colunas para empilhar */
        .stHorizontalBlock > div[data-testid="stHorizontalBlock"] > div {
            width: 100% !important;
            margin-bottom: 1rem;
        }
        
        /* Ajusta o tamanho dos vídeos */
        .stVideo, 
        .stVideo > div, 
        .stVideo > div > video, 
        .stVideo > div > iframe {
            width: 100% !important;
            height: auto !important;
            aspect-ratio: 16/9;
        }
        
        /* Melhora a aparência dos botões em dispositivos móveis */
        .stButton > button {
            padding: 0.5rem 1rem;
            font-size: 0.9em;
        }
    }
    
    /* Ajustes para telas muito pequenas */
    @media (max-width: 480px) {
        .main .block-container {
            padding: 0.5rem;
        }
        
        /* Reduz ainda mais o tamanho da fonte */
        body {
            font-size: 13px;
        }
        
        /* Ajusta o padding dos expanders */
        .streamlit-expanderHeader {
            padding: 0.5rem 0.75rem;
        }
        
        /* Ajusta o tamanho dos títulos */
        h1 { font-size: 1.75rem; }
        h2 { font-size: 1.5rem; }
        h3 { font-size: 1.25rem; }
    }
    
    /* Melhora a aparência das abas em dispositivos móveis */
    @media (max-width: 768px) {
        .stTabs [data-baseweb="tab-list"] {
            display: flex;
            flex-wrap: wrap;
        }
        
        .stTabs [data-baseweb="tab"] {
            flex: 1;
            text-align: center;
            padding: 0.5rem 0.25rem;
        }
    }
    
    /* Ajustes para o player de vídeo responsivo */
    .video-responsive {
        position: relative;
        padding-bottom: 56.25%; /* Proporção 16:9 */
        height: 0;
        overflow: hidden;
        margin: 1rem 0;
        border-radius: 8px;
    }
    
    .video-responsive iframe,
    .video-responsive video {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%; 
        height: 100%;
        border: none;
    }
    
    /* Melhora a aparência dos cards de lição */
    .lesson-card {
        margin-bottom: 1.5rem;
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        transition: transform 0.2s, box-shadow 0.2s;
    }
    
    .lesson-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    
    /* Ajustes para o cabeçalho */
    .main-header {
        padding: 1rem 0;
        margin-bottom: 1.5rem;
        border-bottom: 1px solid #eee;
    }
    
    /* Ajustes para a barra lateral */
    @media (max-width: 768px) {
        .main .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
        }
        
        /* Esconde a barra lateral em telas pequenas */
        section[data-testid="stSidebar"] {
            width: 0 !important;
            min-width: 0 !important;
            transform: translateX(-100%);
            transition: transform 0.3s ease-in-out;
        }
        
        section[data-testid="stSidebar"][aria-expanded="true"] {
            transform: translateX(0);
            width: 75% !important;
            min-width: 0 !important;
            position: fixed;
            z-index: 1000;
            height: 100%;
            background: white;
            box-shadow: 2px 0 8px rgba(0,0,0,0.1);
        }
        
        /* Botão para mostrar/ocultar a barra lateral */
        .sidebar-toggle {
            position: fixed;
            top: 10px;
            left: 10px;
            z-index: 1001;
            background: white;
            border: 1px solid #ddd;
            border-radius: 4px;
            padding: 8px 12px;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
    }
    
    /* Melhora a aparência dos botões de ação */
    .action-button {
        margin: 0.5rem 0;
        width: 100%;
    }
    
    /* Ajustes para o rodapé */
    footer {
        text-align: center;
        padding: 1rem 0;
        margin-top: 2rem;
        border-top: 1px solid #eee;
        font-size: 0.85em;
        color: #666;
    }
    </style>
    """, unsafe_allow_html=True)

def responsive_columns(sizes: List[int] = None, gap: str = '1rem') -> Tuple:
    """
    Cria colunas responsivas que se ajustam ao tamanho da tela.
    
    Args:
        sizes: Lista de tamanhos relativos para cada coluna
        gap: Espaçamento entre as colunas
        
    Returns:
        Tupla de containers para cada coluna
    """
    if sizes is None:
        sizes = [1, 1]  # Padrão: 2 colunas iguais
        
    # Calcula o tamanho total para normalizar
    total = sum(sizes)
    
    # Cria as colunas com base no tamanho da tela
    if st.session_state.get('is_mobile', False):
        # Em dispositivos móveis, empilha as colunas
        return tuple([st.container() for _ in sizes])
    else:
        # Em telas maiores, usa o layout em colunas
        return st.columns(sizes, gap=gap)

def is_mobile() -> bool:
    """Verifica se o dispositivo é móvel com base no user agent."""
    user_agents = [
        'Android', 'webOS', 'iPhone', 'iPad', 'iPod', 
        'BlackBerry', 'Windows Phone', 'Mobile', 'IEMobile'
    ]
    
    # Tenta detectar se é um dispositivo móvel
    user_agent = st.experimental_get_query_params().get('user_agent', [''])[0]
    
    # Se não conseguir detectar, assume que não é móvel
    if not user_agent:
        return False
        
    return any(agent in user_agent for agent in user_agents)

def init_responsive():
    """Inicializa as configurações de responsividade."""
    # Verifica se é um dispositivo móvel
    st.session_state.is_mobile = is_mobile()
    
    # Aplica os estilos responsivos
    apply_responsive_styles()
    
    # Adiciona um botão para alternar a barra lateral em dispositivos móveis
    if st.session_state.is_mobile:
        st.markdown("""
        <style>
        /* Estilo para o botão de alternar a barra lateral */
        .sidebar-toggle {
            position: fixed;
            top: 10px;
            left: 10px;
            z-index: 1001;
            background: white;
            border: 1px solid #ddd;
            border-radius: 4px;
            padding: 8px 12px;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        </style>
        <div class="sidebar-toggle" onclick="document.querySelector('section[data-testid=\'stSidebar\']').setAttribute('aria-expanded', 'true')">
            ☰ Menu
        </div>
        """, unsafe_allow_html=True)
        
        # Fecha a barra lateral ao clicar fora
        st.markdown("""
        <script>
        document.addEventListener('click', function(event) {
            const sidebar = document.querySelector('section[data-testid="stSidebar"]');
            const sidebarToggle = document.querySelector('.sidebar-toggle');
            
            if (sidebar && !sidebar.contains(event.target) && event.target !== sidebarToggle && !sidebarToggle.contains(event.target)) {
                sidebar.setAttribute('aria-expanded', 'false');
            }
        });
        </script>
        """, unsafe_allow_html=True)
