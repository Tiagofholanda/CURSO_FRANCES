"""
Módulo para adicionar medidas de segurança aos vídeos
"""

def get_secure_video_embed(url):
    """
    Retorna um iframe seguro para exibição de vídeos com proteção contra download
    
    Args:
        url (str): URL do vídeo no Google Drive
        
    Returns:
        str: Código HTML do iframe com medidas de segurança
    """
    try:
        if 'drive.google.com' in url:
            file_id = url.split('/file/d/')[1].split('/')[0]
            embed_url = f"https://drive.google.com/file/d/{file_id}/preview"
            
            # Código JavaScript para desabilitar o menu de contexto e teclas de atalho
            security_js = """
            <script>
            // Desabilita o menu de contexto (botão direito do mouse)
            document.addEventListener('contextmenu', function(e) {
                e.preventDefault();
                return false;
            });
            
            // Desabilita teclas de atalho (Ctrl+S, Ctrl+U, F12, etc)
            document.addEventListener('keydown', function(e) {
                // Desabilita F12, Ctrl+Shift+I, Ctrl+Shift+J, Ctrl+U
                if (e.key === 'F12' || 
                   (e.ctrlKey && e.shiftKey && (e.key === 'I' || e.key === 'J' || e.key === 'C' || e.key === 'K')) ||
                   (e.ctrlKey && e.key === 'u') ||
                   (e.ctrlKey && e.key === 's') ||
                   (e.ctrlKey && e.key === 'S') ||
                   (e.ctrlKey && e.shiftKey && e.key === 'C') ||
                   (e.ctrlKey && e.shiftKey && e.key === 'I') ||
                   (e.ctrlKey && e.shiftKey && e.key === 'J') ||
                   (e.ctrlKey && e.shiftKey && e.key === 'K') ||
                   (e.ctrlKey && e.key === 'U')) {
                    e.preventDefault();
                    e.returnValue = false;
                    return false;
                }
            });
            
            // Impede arrastar a imagem do vídeo
            document.addEventListener('dragstart', function(e) {
                if (e.target.tagName === 'IFRAME' || e.target.closest('iframe')) {
                    e.preventDefault();
                    return false;
                }
            });
            
            // Impede a seleção de texto sobre o vídeo
            document.addEventListener('selectstart', function(e) {
                if (e.target.tagName === 'IFRAME' || e.target.closest('iframe')) {
                    e.preventDefault();
                    return false;
                }
            });
            </script>
            """
            
            # Cria o iframe com atributos de segurança
            iframe_html = f"""
            <div style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; border-radius: 8px; margin: 20px 0;" class="video-container">
                <iframe 
                    src="{embed_url}" 
                    style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: none;" 
                    frameborder="0" 
                    scrolling="no"
                    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
                    allowfullscreen
                    oncontextmenu="return false;"
                    onkeydown="return false;"
                    onmousedown="return false;"
                    onselectstart="return false;"
                    ondragstart="return false;"
                    onload="this.contentWindow.document.body.style.pointerEvents='none';"
                ></iframe>
                <div style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;" class="video-overlay"></div>
            </div>
            {security_js}
            """.format(embed_url=embed_url, security_js=security_js)
            
            return iframe_html
            
        elif 'youtube.com' in url or 'youtu.be' in url:
            # Para vídeos do YouTube, usa o modo de privacidade aprimorada
            if 'youtu.be' in url:
                video_id = url.split('/')[-1].split('?')[0]
            else:
                video_id = url.split('v=')[1].split('&')[0]
                
            embed_url = f"https://www.youtube-nocookie.com/embed/{video_id}?rel=0&modestbranding=1&showinfo=0"
            
            return f"""
            <div style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; border-radius: 8px; margin: 20px 0;" class="video-container">
                <iframe 
                    src="{embed_url}" 
                    style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: none;" 
                    frameborder="0" 
                    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
                    allowfullscreen
                    oncontextmenu="return false;"
                ></iframe>
                <div style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;" class="video-overlay"></div>
            </div>
            {security_js}
            """.format(embed_url=embed_url, security_js=security_js)
            
    except Exception as e:
        print(f"Erro ao gerar embed seguro: {str(e)}")
        return f"<p>Não foi possível carregar o vídeo: {str(e)}</p>"
    
    return "<p>URL de vídeo não suportada</p>"
