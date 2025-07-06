import streamlit as st
from typing import Optional, Union, Dict, Any
import base64

class LazyLoader:
    """Classe para gerenciar carregamento preguiçoso de mídia."""
    
    @staticmethod
    def lazy_video(
        video_path: str, 
        format: str = "video/mp4", 
        width: Optional[int] = None,
        start_time: int = 0,
        **kwargs
    ) -> None:
        """
        Exibe um vídeo com carregamento preguiçoso.
        
        Args:
            video_path: Caminho ou URL do vídeo
            format: Formato do vídeo (padrão: video/mp4)
            width: Largura do vídeo (opcional)
            start_time: Tempo de início em segundos (opcional)
            **kwargs: Argumentos adicionais para st.video
        """
        # Se for uma URL, usa o player nativo do Streamlit
        if video_path.startswith(('http://', 'https://')):
            st.video(video_path, format=format, start_time=start_time, **kwargs)
            return
            
        # Para arquivos locais, usa um player personalizado com carregamento preguiçoso
        video_id = f"video-{abs(hash(video_path))}"
        
        st.markdown(f"""
        <div style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden;">
            <video 
                id="{video_id}"
                width="100%" 
                style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"
                controls
                preload="none"
                poster="data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7"
                onclick="this.paused ? this.play() : this.pause();"
            >
                <source src="{video_path}" type="{format}">
                Seu navegador não suporta o elemento de vídeo.
            </video>
        </div>
        <script>
            document.getElementById('{video_id}').addEventListener('click', function() {{
                this.paused ? this.play() : this.pause();
            }});
            
            // Carrega o vídeo quando estiver visível na tela
            const observer = new IntersectionObserver((entries) => {{
                entries.forEach(entry => {{
                    if (entry.isIntersecting) {{
                        const video = entry.target;
                        video.setAttribute('src', video.getAttribute('data-src'));
                        video.load();
                        observer.unobserve(video);
                    }}
                }});
            }}, {{ rootMargin: '200px' }});
            
            observer.observe(document.getElementById('{video_id}'));
        </script>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def lazy_image(
        image_path: str, 
        caption: Optional[str] = None, 
        width: Optional[int] = None,
        use_column_width: Union[bool, str] = False,
        **kwargs
    ) -> None:
        """
        Exibe uma imagem com carregamento preguiçoso.
        
        Args:
            image_path: Caminho ou URL da imagem
            caption: Legenda da imagem (opcional)
            width: Largura da imagem (opcional)
            use_column_width: Se deve usar a largura da coluna
            **kwargs: Argumentos adicionais para st.image
        """
        image_id = f"img-{abs(hash(image_path))}"
        
        # Placeholder base64 transparente
        placeholder = "data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7"
        
        # Se for uma URL, carrega a imagem normalmente
        if image_path.startswith(('http://', 'https://')):
            st.markdown(f"""
            <img 
                id="{image_id}"
                src="{placeholder}" 
                data-src="{image_path}"
                alt="{caption or ''}"
                style="width: {'100%' if use_column_width else (f'{width}px' if width else 'auto')}; 
                       max-width: 100%; 
                       height: auto;"
                class="lazy"
            >
            <script>
                // Carrega a imagem quando estiver visível na tela
                const observer = new IntersectionObserver((entries) => {{
                    entries.forEach(entry => {{
                        if (entry.isIntersectionRatio > 0) {{
                            const img = entry.target;
                            img.src = img.getAttribute('data-src');
                            observer.unobserve(img);
                        }}
                    }});
                }}, {{ rootMargin: '200px' }});
                
                observer.observe(document.getElementById('{image_id}'));
            </script>
            """, unsafe_allow_html=True)
        else:
            # Para arquivos locais, usa o st.image normal
            st.image(image_path, caption=caption, width=width, use_column_width=use_column_width, **kwargs)

# Funções de conveniência
def lazy_video(*args, **kwargs):
    """Função de conveniência para carregamento preguiçoso de vídeos."""
    return LazyLoader.lazy_video(*args, **kwargs)

def lazy_image(*args, **kwargs):
    """Função de conveniência para carregamento preguiçoso de imagens."""
    return LazyLoader.lazy_image(*args, **kwargs)
