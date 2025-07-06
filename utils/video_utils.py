import streamlit as st
from typing import Optional, Dict, Any, Tuple, Union
import re
import base64
from .lazy_loading import LazyLoader

def get_video_embed_url(video_url: str) -> Optional[str]:
    """
    Converte uma URL de vídeo para uma URL de incorporação.
    
    Args:
        video_url: URL do vídeo (YouTube, Vimeo, Google Drive, etc.)
        
    Returns:
        URL de incorporação ou None se não for suportado
    """
    if not video_url or not isinstance(video_url, str):
        return None
        
    video_url = video_url.strip()
    
    # YouTube
    youtube_regex = r'(youtube\.com|youtu\.be|youtube-nocookie\.com)/(watch\?v=|embed/|v/|.+/|\S+?[\w-])'
    youtube_match = re.search(youtube_regex, video_url)
    
    if youtube_match:
        video_id = youtube_match.group(2)
        if video_id.startswith('v='):
            video_id = video_id[2:]
        elif '/' in video_id:
            video_id = video_id.split('/')[-1]
        return f"https://www.youtube.com/embed/{video_id}?autoplay=0&modestbranding=1&rel=0"
    
    # Vimeo
    vimeo_regex = r'vimeo\.com/(\d+)'
    vimeo_match = re.search(vimeo_regex, video_url)
    
    if vimeo_match:
        video_id = vimeo_match.group(1)
        return f"https://player.vimeo.com/video/{video_id}?title=0&byline=0&portrait=0"
    
    # Google Drive
    drive_regex = r'drive\.google\.com/file/d/([a-zA-Z0-9_-]+)'
    drive_match = re.search(drive_regex, video_url)
    
    if drive_match:
        file_id = drive_match.group(1)
        return f"https://drive.google.com/file/d/{file_id}/preview"
    
    # Se não for um dos formatos suportados, retorna a URL original
    return video_url

def display_video(
    video_url: str,
    width: int = 0,
    height: int = 0,
    autoplay: bool = False,
    controls: bool = True,
    lazy: bool = True
) -> None:
    """
    Exibe um vídeo de forma responsiva com suporte a múltiplas fontes.
    
    Args:
        video_url: URL do vídeo ou caminho local
        width: Largura do vídeo (0 para responsivo)
        height: Altura do vídeo (0 para proporção 16:9)
        autoplay: Se o vídeo deve iniciar automaticamente
        controls: Se deve mostrar os controles do player
        lazy: Se deve usar carregamento preguiçoso
    """
    if not video_url:
        st.warning("Nenhum URL de vídeo fornecido.")
        return
    
    # Obtém a URL de incorporação
    embed_url = get_video_embed_url(video_url)
    
    if not embed_url:
        st.error("Formato de URL de vídeo não suportado.")
        return
    
    # Configura os parâmetros da URL
    if '?' in embed_url:
        embed_url += '&'
    else:
        embed_url += '?'
    
    params = []
    if autoplay:
        params.append('autoplay=1')
    else:
        params.append('autoplay=0')
    
    if not controls:
        params.append('controls=0')
    
    embed_url += '&'.join(params)
    
    # Define o estilo CSS responsivo
    if width > 0 and height > 0:
        aspect_ratio = height / width * 100
        style = f"position: relative; padding-bottom: {aspect_ratio}%; height: 0; overflow: hidden;"
    else:
        style = "position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden;"  # 16:9
    
    # Gera o HTML do player de vídeo
    video_html = f"""
    <div style="{style}">
        <iframe 
            src="{embed_url}" 
            style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: none;"
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
            allowfullscreen>
        </iframe>
    </div>
    """
    
    # Exibe o vídeo usando o carregamento preguiçoso se solicitado
    if lazy and 'youtube.com' not in embed_url and 'youtu.be' not in embed_url:
        LazyLoader.lazy_video(embed_url, width=width, autoplay=autoplay, controls=controls)
    else:
        st.components.v1.html(video_html, height=height if height > 0 else 450)

def get_video_thumbnail(video_url: str) -> Optional[str]:
    """
Módulo para manipulação de vídeos no Curso de Francês.
"""
    if 'youtube.com' in video_url or 'youtu.be' in video_url:
        if 'youtube.com' in video_url:
        if 'youtube.com/watch' in video_url:
            video_id = video_url.split('v=')[1].split('&')[0]
        elif 'youtu.be/' in video_url:
            video_id = video_url.split('youtu.be/')[1].split('?')[0]
        
        if video_id:
            return f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg"
    
    # Para outros tipos de vídeo, retorna None (não há suporte para miniaturas)
    return None

def create_video_card(
    video_url: str,
    title: str = "",
    description: str = "",
    width: int = 0,
    height: int = 0,
    show_thumbnail: bool = True,
    show_title: bool = True,
    show_description: bool = True,
    show_controls: bool = True
) -> None:
    """
    Cria um card de vídeo estilizado com informações adicionais.
    
    Args:
        video_url: URL do vídeo
        title: Título do vídeo
        description: Descrição do vídeo
        width: Largura do card (0 para largura total)
        height: Altura do vídeo (0 para proporção 16:9)
        show_thumbnail: Se deve mostrar a miniatura do vídeo
        show_title: Se deve mostrar o título do vídeo
        show_description: Se deve mostrar a descrição do vídeo
        show_controls: Se deve mostrar os controles do player
    """
    # Cria um container para o card
    with st.container():
        col1, col2 = st.columns([1, 3]) if width > 0 else st.columns([1])
        
        with col1 if width > 0 else st:
            if show_thumbnail:
                thumbnail_url = get_video_thumbnail(video_url)
                if thumbnail_url:
                    st.image(thumbnail_url, use_column_width=True)
        
        with col2 if width > 0 else st:
            if show_title and title:
                st.subheader(title)
            
            if show_description and description:
                st.caption(description)
            
            # Exibe o vídeo
            display_video(
                video_url,
                width=width,
                height=height,
                controls=show_controls,
                lazy=True
            )
