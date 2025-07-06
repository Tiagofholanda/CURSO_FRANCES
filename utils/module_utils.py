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
            
            /* Melhora botões */
            .stButton > button {
                width: 100%;
                margin: 0.25rem 0;
            }
            
            /* Ajusta os títulos */
            h1 {
                font-size: 1.75rem !important;
            }
            
            h2 {
                font-size: 1.5rem !important;
            }
            
            h3 {
                font-size: 1.25rem !important;
            }
            
            /* Melhora a barra lateral em dispositivos móveis */
            [data-testid="stSidebar"] {
                width: 85% !important;
                min-width: 200px !important;
                max-width: 300px !important;
            }
            
            /* Ajusta o menu de navegação */
            .css-1d391kg {
                padding: 0.5rem;
            }
            
            /* Melhora a exibição de mensagens de erro/sucesso */
            .stAlert {
                margin: 0.5rem 0;
            }
        }
        
        /* Melhorias gerais para todos os dispositivos */
        .stVideo iframe {
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        
        /* Ajusta o container principal para evitar quebras de layout */
        .main .block-container {
            max-width: 1200px;
            padding: 2rem 2rem 12rem;
        }
        
        /* Melhora a experiência de toque em dispositivos móveis */
        button, [role="button"], a {
            touch-action: manipulation;
        }
        
        /* Previne zoom em campos de input em iOS */
        @media screen and (-webkit-min-device-pixel-ratio:0) { 
            input, select, textarea { 
                font-size: 16px !important;
            }
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Carrega o CSS personalizado
    load_css()

def display_progress_bar(module_name: str, total_lessons: int):
    """Exibe a barra de progresso do módulo"""
    if 'username' not in st.session_state:
        return
        
    progress = UserProgress.get_module_progress(module_name, total_lessons)
    completed = int(progress / 100 * total_lessons)
    
    st.markdown(f"""
    <div class="progress-container">
        <div class="progress-header">
            <h3 class="progress-title">Seu Progresso</h3>
            <span class="progress-percent">{progress:.0f}%</span>
        </div>
        <div class="progress-bar">
            <div class="progress-fill" style="width: {progress}%;"></div>
        </div>
        <div class="progress-stats">
            <span>{completed} de {total_lessons} lições concluídas</span>
            <span>{total_lessons - completed} restantes</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

def get_module_lessons(spreadsheet_url: str, module_name: str) -> Dict[str, List[Dict[str, Any]]]:
    """
    Obtém as lições de um módulo específico com cache
    
    Args:
        spreadsheet_url: URL da planilha do Google Sheets
        module_name: Nome do módulo para filtrar as lições
        
    Returns:
        Dicionário com as lições do módulo
    """
    def load_data():
        try:
            df = load_excel_from_google_drive(spreadsheet_url)
            if df is None or df.empty:
                st.error("Não foi possível carregar os dados da planilha.")
                return {}
                
            # Verifica colunas obrigatórias
            required_columns = ['Módulo', 'Título da Aula', 'Link do Vídeo', 'Link do Documento', 'Duração', 'ordem']
            missing_columns = [col for col in required_columns if col not in df.columns]
            
            if missing_columns:
                st.error(f"Colunas ausentes na planilha: {', '.join(missing_columns)}")
                return {}
                
            # Filtra pelo módulo (case insensitive)
            module_df = df[df['Módulo'].str.strip().str.lower() == module_name.lower()]
            
            if module_df.empty:
                st.warning(f"Nenhuma lição encontrada para o módulo '{module_name}'.")
                return {}
                
            # Ordena as lições
            module_df = module_df.sort_values('ordem')
            
            # Converte para o formato de dicionário
            lessons = []
            for _, row in module_df.iterrows():
                lesson = {
                    'id': f"{module_name.lower()}_{row['ordem']}",
                    'title': row['Título da Aula'].strip(),
                    'video_url': str(row['Link do Vídeo']).strip(),
                    'doc_url': str(row['Link do Documento']).strip(),
                    'duration': str(row['Duração']).strip(),
                    'order': int(row['ordem'])
                }
                lessons.append(lesson)
                
            return {'lessons': lessons}
            
        except Exception as e:
            st.error(f"Erro ao carregar as lições: {str(e)}")
            import traceback
            st.error(traceback.format_exc())
            return {}
    
    # Usa o cache para carregar os dados
    from .user_progress import load_cached_data
    return load_cached_data(spreadsheet_url, load_data)

def display_lesson(lesson: Dict[str, Any], module_name: str):
    """
    Exibe uma lição com vídeo, material de apoio e opção de marcação como concluída
    
    Args:
        lesson: Dicionário com os dados da lição
        module_name: Nome do módulo para controle de progresso
    """
    # Verifica se a lição está concluída
    is_complete = UserProgress.is_lesson_complete(lesson['id'], module_name)
    
    # Define as classes CSS baseadas no status de conclusão
    card_class = "lesson-card" + (" completed" if is_complete else "")
    
    # Cria o cabeçalho da lição
    st.markdown(f"""
    <div class="{card_class}">
        <div class="lesson-header">
            <h3>{lesson['title']}</h3>
            <span class="lesson-duration">⏱️ {lesson['duration']}</span>
        </div>
    """, unsafe_allow_html=True)
    
    # Exibe o vídeo se houver URL
    video_placeholder = st.empty()
    if lesson.get('video_url') and pd.notna(lesson['video_url']) and lesson['video_url'].strip():
        try:
            video_url = lesson['video_url'].strip()
            
            # Extrai o ID do vídeo do YouTube ou Google Drive
            if 'youtube.com' in video_url or 'youtu.be' in video_url:
                # Extrai ID do YouTube
                if 'youtube.com' in video_url:
                    video_id = video_url.split('v=')[1].split('&')[0]
                else:  # youtu.be
                    video_id = video_url.split('/')[-1]
                embed_url = f"https://www.youtube.com/embed/{video_id}?rel=0&modestbranding=1"
                
                video_html = f"""
                <div class="video-container">
                    <iframe src="{embed_url}" 
                            frameborder="0"
                            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
                            allowfullscreen>
                    </iframe>
                </div>
                """
                video_placeholder.markdown(video_html, unsafe_allow_html=True)
                
            elif 'drive.google.com' in video_url:
                # Extrai ID do Google Drive
                file_id = video_url.split('/file/d/')[1].split('/')[0]
                embed_url = f"https://drive.google.com/file/d/{file_id}/preview"
                
                video_html = f"""
                <div class="video-container">
                    <iframe src="{embed_url}" 
                            frameborder="0"
                            allow="autoplay" 
                            allowfullscreen>
                    </iframe>
                </div>
                """
                video_placeholder.markdown(video_html, unsafe_allow_html=True)
                
        except Exception as e:
            st.warning("Não foi possível carregar o vídeo desta lição.")
            print(f"Erro ao carregar vídeo: {str(e)}")
    
    # Seção de materiais e ações
    with st.container():
        col1, col2 = st.columns([1, 2])
        
        with col1:
            # Botão para marcar/desmarcar como concluído
            new_status = st.checkbox(
                "✅ Marcar como concluído" if is_complete else "☑️ Marcar como concluído",
                value=is_complete,
                key=f"complete_{lesson['id']}",
                on_change=lambda: UserProgress.toggle_lesson_complete(lesson['id'], module_name)
            )
            
            # Atualiza o status se mudar
            if new_status != is_complete:
                UserProgress.toggle_lesson_complete(lesson['id'], module_name)
                st.rerun()
        
        with col2:
            # Botão para baixar material (se houver)
            if lesson.get('doc_url') and pd.notna(lesson['doc_url']) and lesson['doc_url'].strip():
                try:
                    doc_url = lesson['doc_url'].strip()
                    if 'drive.google.com' in doc_url:
                        # Extrai o ID do arquivo do Google Drive
                        if '/file/d/' in doc_url:
                            file_id = doc_url.split('/file/d/')[1].split('/')[0]
                        else:  # Para links de compartilhamento
                            file_id = doc_url.split('id=')[1].split('&')[0]
                        download_url = f"https://drive.google.com/uc?export=download&id={file_id}"
                        view_url = f"https://drive.google.com/file/d/{file_id}/view"
                    else:
                        download_url = doc_url
                        view_url = doc_url
                    
                    st.markdown(f"""
                    <div class="material-actions">
                        <a href="{download_url}" class="btn" download>
                            <span class="material-icons">download</span> Baixar Material
                        </a>
                        <a href="{view_url}" class="btn btn-outline" target="_blank">
                            <span class="material-icons">visibility</span> Visualizar
                        </a>
                    </div>
                    """, unsafe_allow_html=True)
                except Exception as e:
                    st.warning("Não foi possível carregar o material desta lição.")
                    print(f"Erro ao carregar material: {str(e)}")
    
    # Fecha a div do card da lição
    st.markdown("</div>", unsafe_allow_html=True)

def get_modules_data(spreadsheet_url):
    """
    Carrega os dados da planilha e retorna um dicionário com os módulos
    """
    df = load_excel_from_google_drive(spreadsheet_url)
    if df.empty:
        return {}
    
    # Garante que as colunas necessárias existam
    required_columns = ['Módulo', 'Título da Aula', 'Link do Vídeo', 'Link do Documento']
    for col in required_columns:
        if col not in df.columns:
            st.error(f"Coluna obrigatória não encontrada: {col}")
            return {}
    
    # Remove linhas sem link de vídeo
    df = df.dropna(subset=['Link do Vídeo'])
    
    # Agrupa por módulo
    modules = {}
    for _, row in df.iterrows():
        module_name = row['Módulo']
        if pd.isna(module_name):
            module_name = "Outros"
        
        if module_name not in modules:
            modules[module_name] = []
        
        modules[module_name].append({
            'title': row['Título da Aula'],
            'video_url': row['Link do Vídeo'],
            'doc_url': row.get('Link do Documento', ''),
            'duration': row.get('Duração', ''),
            'order': row.get('ordem', 0)
        })
    
    # Ordena os itens de cada módulo
    for module in modules:
        modules[module].sort(key=lambda x: x.get('order', 0))
    
    return modules
