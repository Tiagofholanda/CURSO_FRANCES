"""
Módulo de utilidades para o Curso de Francês.

Este pacote contém várias utilidades para melhorar a performance, acessibilidade e responsividade do aplicativo.
"""

# Importações dos módulos
from .accessibility_utils import (
    apply_accessibility_settings,
    add_skip_link,
    add_aria_labels,
    init_accessibility
)

from .lazy_loading import (
    LazyLoader,
    lazy_video,
    lazy_image
)

from .performance_utils import (
    memoize_with_ttl,
    cached_dataframe,
    cached_text,
    cached_computation,
    clear_cache,
    get_cache_size
)

from .responsive_utils import (
    apply_responsive_styles,
    responsive_columns,
    is_mobile,
    init_responsive
)

from .video_utils import (
    get_video_embed_url,
    display_video,
    get_video_thumbnail,
    create_video_card
)

# Exporta as funções principais
__all__ = [
    # Acessibilidade
    'apply_accessibility_settings',
    'add_skip_link',
    'add_aria_labels',
    'init_accessibility',
    
    # Carregamento preguiçoso
    'LazyLoader',
    'lazy_video',
    'lazy_image',
    
    # Performance
    'memoize_with_ttl',
    'cached_dataframe',
    'cached_text',
    'cached_computation',
    'clear_cache',
    'get_cache_size',
    
    # Responsividade
    'apply_responsive_styles',
    'responsive_columns',
    'is_mobile',
    'init_responsive',
    
    # Vídeos
    'get_video_embed_url',
    'display_video',
    'get_video_thumbnail',
    'create_video_card'
]
