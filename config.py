"""
Configurações globais do aplicativo.

Este módulo contém as configurações globais usadas em todo o aplicativo.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Diretórios
BASE_DIR = Path(__file__).parent.absolute()
DATA_DIR = BASE_DIR / 'data'
CACHE_DIR = BASE_DIR / '.cache'
ASSETS_DIR = BASE_DIR / 'assets'
PAGES_DIR = BASE_DIR / 'pages'

# Cria os diretórios necessários
for directory in [DATA_DIR, CACHE_DIR, ASSETS_DIR, PAGES_DIR]:
    directory.mkdir(exist_ok=True, parents=True)

# Configurações do aplicativo
APP_NAME = "Curso de Francês"
APP_DESCRIPTION = "Aplicativo interativo para aprendizado de francês"
APP_VERSION = "1.0.0"

# Configurações de cache
CACHE_TTL = 3600  # 1 hora em segundos
MAX_CACHE_SIZE = 100 * 1024 * 1024  # 100 MB

# Configurações de acessibilidade
DEFAULT_FONT_SIZE = 16  # px
HIGH_CONTRAST_MODE = False
DARK_MODE = False

# Configurações de vídeo
DEFAULT_VIDEO_WIDTH = 800
DEFAULT_VIDEO_HEIGHT = 450  # 16:9 aspect ratio

# Configurações de responsividade
MOBILE_BREAKPOINT = 768  # px
TABLET_BREAKPOINT = 1024  # px

# Configurações do Google Sheets (opcional)
GOOGLE_SHEETS_CREDENTIALS = os.getenv('GOOGLE_SHEETS_CREDENTIALS')
GOOGLE_SHEET_ID = os.getenv('GOOGLE_SHEET_ID')

# Configurações de autenticação (opcional)
AUTH_ENABLED = os.getenv('AUTH_ENABLED', 'false').lower() == 'true'
AUTH_USERNAME = os.getenv('AUTH_USERNAME', 'admin')
AUTH_PASSWORD = os.getenv('AUTH_PASSWORD', 'password')

# Configurações de log
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_FILE = BASE_DIR / 'app.log'

# Configurações de tema
THEME = {
    'primary_color': '#1E88E5',
    'secondary_color': '#1565C0',
    'background_color': '#FFFFFF',
    'secondary_background': '#F5F5F5',
    'text_color': '#333333',
    'font': 'sans-serif',
    'border_radius': '8px',
    'box_shadow': '0 2px 4px rgba(0, 0, 0, 0.1)',
}

# Configurações de mídia social
SOCIAL_MEDIA = {
    'twitter': 'https://twitter.com/seusite',
    'facebook': 'https://facebook.com/seusite',
    'instagram': 'https://instagram.com/seusite',
    'youtube': 'https://youtube.com/seusite',
}

# Configurações de contato
CONTACT_EMAIL = 'contato@cursofrances.com.br'
CONTACT_PHONE = '+55 (11) 1234-5678'

# Configurações de privacidade
PRIVACY_POLICY_URL = 'https://seusite.com/privacidade'
TERMS_OF_SERVICE_URL = 'https://seusite.com/termos'

# Configurações de análise (opcional)
GOOGLE_ANALYTICS_ID = os.getenv('GOOGLE_ANALYTICS_ID', '')

# Configurações de CDN (opcional)
USE_CDN = os.getenv('USE_CDN', 'false').lower() == 'true'
CDN_URL = os.getenv('CDN_URL', 'https://cdn.seusite.com')

def get_asset_path(filename: str) -> str:
    """Retorna o caminho completo para um arquivo na pasta de assets."""
    return str(ASSETS_DIR / filename)

def get_cache_path(filename: str) -> str:
    """Retorna o caminho completo para um arquivo na pasta de cache."""
    return str(CACHE_DIR / filename)

def get_data_path(filename: str) -> str:
    """Retorna o caminho completo para um arquivo na pasta de dados."""
    return str(DATA_DIR / filename)

# Cria um dicionário com todas as configurações para facilitar a exportação
settings = {
    key: value for key, value in globals().items() 
    if key.isupper() and not key.startswith('_')
}
