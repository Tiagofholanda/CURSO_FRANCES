import pandas as pd
import streamlit as st
from .excel_utils import load_excel_from_google_drive
from .user_progress import UserProgress, DataCache
from typing import Dict, List, Any, Optional, Callable
import re
import time
from datetime import datetime

def load_css():
    """Carrega o arquivo CSS com os estilos personalizados"""
    with open("assets/styles.css", "r") as f:
        css = f.read()
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

def apply_responsive_styles():
    """Aplica estilos CSS para melhorar a responsividade em dispositivos móveis"""
    st.markdown("""
    <style>
        /* Estilos gerais para dispositivos móveis */
        @media (max-width: 768px) {
            /* Ajusta o padding do conteúdo principal */
            .main .block-container {
                padding: 1rem 1rem 10rem;
            }
            
            /* Melhora a visualização dos expanders */
            .streamlit-expanderHeader {
                font-size: 1rem;
                padding: 0.75rem 1rem;
            }
            
            /* Ajusta o player de vídeo */
            .stVideo {
                position: relative;
                padding-bottom: 56.25%; /* Proporção 16:9 */
                height: 0;
                overflow: hidden;
                margin: 1rem 0;
            }
            
            .stVideo iframe {
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                border: none;
            }
        }
    </style>
    """, unsafe_allow_html=True)

def display_progress_bar(module_name: str, total_lessons: int):
    """Exibe a barra de progresso do módulo"""
    progress = UserProgress.get_instance()
    completed = progress.get_completed_lessons(module_name)
    progress_percent = int((len(completed) / total_lessons) * 100) if total_lessons > 0 else 0
    
    st.progress(progress_percent)
    st.caption(f"{len(completed)} de {total_lessons} lições concluídas ({progress_percent}%)")

def get_module_lessons(spreadsheet_url: str, module_name: str) -> Dict[str, Any]:
    """
    Obtém as lições de um módulo específico com cache
    
    Args:
        spreadsheet_url: URL da planilha do Google Sheets
        module_name: Nome do módulo para filtrar as lições
        
    Returns:
        Dicionário com as lições do módulo
    """
    cache = DataCache.get_instance()
    cache_key = f"{spreadsheet_url}_{module_name}"
    
    # Tenta obter os dados do cache
    cached_data = cache.get(cache_key)
    if cached_data is not None:
        return cached_data
    
    try:
        # Carrega a planilha
        df = load_excel_from_google_drive(spreadsheet_url)
        
        # Filtra as lições do módulo
        module_df = df[df['Módulo'] == module_name].copy()
        
        if module_df.empty:
            return {
                'module_name': module_name,
                'lessons': [],
                'total_lessons': 0,
                'last_updated': datetime.now().isoformat()
            }
        
        # Ordena as lições pela coluna 'ordem'
        module_df = module_df.sort_values(by='ordem')
        
        # Processa as lições
        lessons = []
        for _, row in module_df.iterrows():
            # Função auxiliar para limpar strings
            def clean_string(value, default=''):
                if pd.isna(value) or value is None:
                    return default
                try:
                    return str(value).strip()
                except:
                    return default
            
            # Função para extrair ID do Google Drive
            def extract_google_drive_id(url):
                if not url or pd.isna(url):
                    return None
                try:
                    if 'drive.google.com' in str(url):
                        if '/file/d/' in str(url):
                            return str(url).split('/file/d/')[1].split('/')[0].split('?')[0]
                        elif 'id=' in str(url):
                            return str(url).split('id=')[1].split('&')[0]
                except:
                    pass
                return None
            
            # Processa os dados da linha
            order = int(row['ordem']) if pd.notna(row.get('ordem')) and str(row['ordem']).isdigit() else 0
            video_url = clean_string(row.get('Link do Vídeo'))
            doc_url = clean_string(row.get('Link do Documento'))
            
            lesson = {
                'id': f"{module_name.lower()}_{order}",
                'title': clean_string(row.get('Título da Aula', 'Sem título')),
                'video_url': video_url,
                'video_id': extract_google_drive_id(video_url),
                'doc_url': doc_url,
                'doc_id': extract_google_drive_id(doc_url),
                'duration': clean_string(row.get('Duração', '00:00')),
                'order': order,
                'level': clean_string(row.get('Nível', 'Iniciante'))
            }
            lessons.append(lesson)
        
        # Prepara o resultado
        result = {
            'module_name': module_name,
            'lessons': lessons,
            'total_lessons': len(lessons),
            'last_updated': datetime.now().isoformat()
        }
        
        # Salva no cache
        cache.set(cache_key, result, timeout=3600)  # Cache por 1 hora
        
        return result
        
    except Exception as e:
        st.error(f"Erro ao carregar as lições: {str(e)}")
        return {
            'module_name': module_name,
            'lessons': [],
            'total_lessons': 0,
            'last_updated': datetime.now().isoformat(),
            'error': str(e)
        }

def display_lesson(lesson: Dict[str, Any], module_name: str):
    """
    Exibe uma lição com vídeo, material de apoio e opção de marcação como concluída
    
    Args:
        lesson: Dicionário com os dados da lição
        module_name: Nome do módulo para controle de progresso
    """
    # Cria um container para a lição
    with st.container():
        # Cabeçalho da lição
        st.markdown(f"### {lesson['title']}")
        
        # Exibe o vídeo se houver URL
        video_placeholder = st.empty()
        video_id = lesson.get('video_id')
        
        if video_id:
            try:
                # Determina se é um vídeo do YouTube ou Google Drive
                if 'youtube.com' in str(lesson.get('video_url', '')) or 'youtu.be' in str(lesson.get('video_url', '')):
                    embed_url = f"https://www.youtube.com/embed/{video_id}?rel=0&modestbranding=1"
                    fallback_url = f"https://youtu.be/{video_id}"
                    source_name = "YouTube"
                else:
                    embed_url = f"https://drive.google.com/file/d/{video_id}/preview"
                    fallback_url = f"https://drive.google.com/file/d/{video_id}/view"
                    source_name = "Google Drive"
                
                # HTML para o player de vídeo
                video_html = f"""
                <style>
                .video-container {{
                    position: relative;
                    padding-bottom: 56.25%; /* Proporção 16:9 */
                    height: 0;
                    overflow: hidden;
                    max-width: 100%;
                    margin: 1rem 0;
                    border-radius: 8px;
                    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
                    background: #f5f5f5;
                }}
                .video-container iframe {{
                    position: absolute;
                    top: 0;
                    left: 0;
                    width: 100%;
                    height: 100%;
                    border: none;
                }}
                .video-placeholder {{
                    position: absolute;
                    top: 0;
                    left: 0;
                    width: 100%;
                    height: 100%;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    background: linear-gradient(135deg, #f5f7fa 0%, #e4e8eb 100%);
                    color: #666;
                    font-size: 1rem;
                    text-align: center;
                    padding: 2rem;
                    box-sizing: border-box;
                    border-radius: 8px;
                }}
                .video-placeholder a {{
                    color: #4361ee;
                    text-decoration: none;
                    font-weight: 500;
                }}
                .video-placeholder a:hover {{
                    text-decoration: underline;
                }}
                </style>
                <div class="video-container">
                    <iframe src="{embed_url}" 
                            frameborder="0"
                            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
                            allowfullscreen>
                    </iframe>
                    <div class="video-placeholder" style="display: none;">
                        <div>
                            <p>Carregando vídeo do {source_name}...</p>
                            <p>Se o vídeo não carregar, tente acessar o <a href="{fallback_url}" target="_blank" rel="noopener noreferrer">link direto</a>.</p>
                        </div>
                    </div>
                </div>
                <script>
                // Adiciona um fallback caso o iframe não carregue
                document.addEventListener('DOMContentLoaded', function() {{
                    const iframe = document.querySelector('.video-container iframe');
                    const placeholder = document.querySelector('.video-placeholder');
                    
                    if (iframe) {{
                        iframe.onload = function() {{
                            if (placeholder) {{
                                placeholder.style.display = 'none';
                            }}
                        }};
                        
                        // Mostra o placeholder se o iframe não carregar em 5 segundos
                        setTimeout(function() {{
                            if (iframe.offsetParent === null || 
                                iframe.offsetWidth === 0 || 
                                iframe.offsetHeight === 0) {{
                                if (placeholder) {{
                                    placeholder.style.display = 'flex';
                                }}
                            }}
                        }}, 5000);
                    }} else if (placeholder) {{
                        placeholder.style.display = 'flex';
                    }}
                }});
                </script>
                """
                video_placeholder.markdown(video_html, unsafe_allow_html=True)
                
            except Exception as e:
                video_placeholder.error(f"❌ Não foi possível carregar o vídeo desta lição. Erro: {str(e)}")
                print(f"Erro ao carregar vídeo: {str(e)}")
        else:
            video_placeholder.info("ℹ️ Nenhum vídeo disponível para esta lição.")
        
        # Seção de materiais e ações
        with st.container():
            st.markdown("---")
            col1, col2 = st.columns([1, 1])
            
            with col1:
                # Material de apoio
                if lesson.get('doc_url'):
                    st.markdown("### 📚 Material de Apoio")
                    st.markdown(f"[Abrir material](#)")
            
            with col2:
                # Opção de marcar como concluído
                progress = UserProgress.get_instance()
                completed = progress.is_lesson_completed(module_name, lesson['id'])
                
                if st.checkbox("Marcar como concluído", value=completed, key=f"completed_{lesson['id']}"):
                    progress.complete_lesson(module_name, lesson['id'])
                    st.success("✓ Lição marcada como concluída!")
                else:
                    progress.uncomplete_lesson(module_name, lesson['id'])

def get_modules_data(spreadsheet_url: str) -> Dict[str, Any]:
    """
    Carrega os dados da planilha e retorna um dicionário com os módulos
    """
    try:
        # Carrega a planilha
        df = load_excel_from_google_drive(spreadsheet_url)
        
        # Obtém a lista de módulos únicos
        modules = df['Módulo'].unique().tolist()
        
        # Prepara o resultado
        result = {
            'modules': [],
            'total_modules': len(modules),
            'last_updated': datetime.now().isoformat()
        }
        
        # Para cada módulo, obtém as lições
        for module_name in modules:
            if pd.isna(module_name):
                continue
                
            module_data = get_module_lessons(spreadsheet_url, module_name)
            result['modules'].append({
                'name': module_name,
                'total_lessons': module_data.get('total_lessons', 0),
                'last_updated': module_data.get('last_updated', datetime.now().isoformat())
            })
        
        return result
        
    except Exception as e:
        st.error(f"Erro ao carregar os dados dos módulos: {str(e)}")
        return {
            'modules': [],
            'total_modules': 0,
            'last_updated': datetime.now().isoformat(),
            'error': str(e)
        }
