import pandas as pd
import streamlit as st
from .excel_utils import load_excel_from_google_drive
from .user_progress import UserProgress, DataCache
from typing import Dict, List, Any, Optional, Callable
import re
import time
from datetime import datetime

def load_css():
    """Carrega os estilos CSS diretamente no código"""
    css = """
    /* Estilos básicos */
    :root {
        --primary-color: #4a6fa5;
        --secondary-color: #166088;
        --accent-color: #4fc3a1;
        --background-color: #f8f9fa;
        --text-color: #333333;
        --border-radius: 8px;
        --box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    /* Estilos gerais */
    body {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        line-height: 1.6;
        color: var(--text-color);
        background-color: var(--background-color);
    }
    
    /* Estilos para dispositivos móveis */
    @media (max-width: 768px) {
        .main .block-container {
            padding: 1rem 1rem 10rem;
        }
        
        .streamlit-expanderHeader {
            font-size: 1rem;
            padding: 0.75rem 1rem;
        }
        
        .stVideo {
            position: relative;
            padding-bottom: 56.25%;
            height: 0;
            overflow: hidden;
            margin: 1rem 0;
        }
    }
    """
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

def display_page_header(module_name: str, icon: str, description: str, total_lessons: int = 0):
    """
    Exibe o cabeçalho padronizado da página com barra de progresso
    
    Args:
        module_name: Nome do módulo (em minúsculas, sem acentos)
        icon: Ícone do módulo (emoji)
        description: Breve descrição do módulo
        total_lessons: Número total de lições no módulo (opcional)
    """
    # Formata o nome do módulo para exibição
    display_name = module_name.capitalize()
    
    # Exibe o cabeçalho
    st.markdown(f"""
    <div class="header">
        <h1>{icon} {display_name} Francês</h1>
        <p>{description}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Exibe a barra de progresso se houver lições
    if total_lessons > 0 and 'username' in st.session_state:
        display_progress_bar(module_name, total_lessons)

def display_progress_bar(module_name: str, total_lessons: int, progress: int = 0):
    """
    Exibe a barra de progresso do módulo
    
    Args:
        module_name: Nome do módulo
        total_lessons: Número total de lições
        progress: Porcentagem de conclusão (0-100)
    """
    if total_lessons == 0:
        return
        
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
                youtube_url = clean_string(row.get('link extra youtube', ''))
                
                lesson = {
                    'id': f"{module_name.lower()}_{order}",
                    'title': clean_string(row.get('Título da Aula', 'Sem título')),
                    'video_url': video_url,
                    'video_id': extract_google_drive_id(video_url),
                    'doc_url': doc_url,
                    'doc_id': extract_google_drive_id(doc_url),
                    'youtube_url': youtube_url,
                    'duration': clean_string(row.get('Duração', '00:00')),
                    'order': order,
                    'level': clean_string(row.get('Nível', 'Iniciante'))
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
    try:
        # Verifica se a lição está concluída
        is_complete = UserProgress.is_lesson_complete(lesson['id'], module_name)
        
        # Define as classes CSS baseadas no status de conclusão
        card_class = "lesson-card" + (" completed" if is_complete else "")
        
        # Cria o cabeçalho da lição com animação e efeitos
        st.markdown(f"""
        <div class="{card_class}" data-aos="fade-up">
            <div class="lesson-header">
                <div class="header-content">
                    <h3>{lesson['title']}</h3>
                    <div class="lesson-meta">
                        <span class="lesson-duration">
                            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                                <circle cx="12" cy="12" r="10"></circle>
                                <polyline points="12 6 12 12 16 14"></polyline>
                            </svg>
                            {lesson.get('duration', '')}
                        </span>
                        <span class="lesson-level">
                            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                                <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
                                <polyline points="22 4 12 14.01 9 11.01"></polyline>
                            </svg>
                            {lesson.get('level', 'Iniciante')}
                        </span>
                    </div>
                </div>
                <div class="lesson-actions">
                    <button class="action-btn favorite" title="Favoritar">
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                            <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"></path>
                        </svg>
                    </button>
                    <button class="action-btn share" title="Compartilhar">
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                            <circle cx="18" cy="5" r="3"></circle>
                            <circle cx="6" cy="12" r="3"></circle>
                            <circle cx="18" cy="19" r="3"></circle>
                            <line x1="8.59" y1="13.51" x2="15.42" y2="17.49"></line>
                            <line x1="15.41" y1="6.51" x2="8.59" y2="10.49"></line>
                        </svg>
                    </button>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
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
                
                # Tenta incorporar o vídeo diretamente
                try:
                    # Para vídeos do YouTube
                    if 'youtube.com' in str(lesson.get('video_url', '')) or 'youtu.be' in str(lesson.get('video_url', '')):
                        st.video(lesson.get('video_url'))
                    # Para vídeos do Google Drive
                    elif 'drive.google.com' in str(lesson.get('video_url', '')):
                        video_id = lesson.get('video_id', '')
                        if video_id:
                            embed_url = f"https://drive.google.com/file/d/{video_id}/preview"
                            st.components.v1.iframe(embed_url, height=500)
                    else:
                        # Para outros tipos de vídeo
                        st.video(lesson.get('video_url'))
                except Exception as e:
                    # Se houver erro na incorporação, mostra o link
                    st.warning("Não foi possível carregar o vídeo incorporado.")
                    st.markdown(f"""
                    <div style="padding: 1rem; background-color: #f8f9fa; border-radius: 8px; margin: 1rem 0;">
                        <p>Para assistir ao vídeo, clique no link abaixo:</p>
                        <a href="{fallback_url}" target="_blank" rel="noopener noreferrer" 
                           style="display: inline-block; padding: 0.5rem 1rem; background-color: #4361ee; 
                                  color: white; text-decoration: none; border-radius: 4px;">
                            Assistir vídeo no {source_name}
                        </a>
                    </div>
                    """, unsafe_allow_html=True)
                
            except Exception as e:
                video_placeholder.error(f"❌ Não foi possível carregar o vídeo desta lição. Erro: {str(e)}")
                print(f"Erro ao carregar vídeo: {str(e)}")
        else:
            video_placeholder.info("ℹ️ Nenhum vídeo disponível para esta lição.")
        
        # Seção de materiais e ações
        with st.container():
            col1, col2 = st.columns([1, 2])
            
            with col1:
                # Botão para marcar/desmarcar como concluído com efeito moderno
                st.markdown("""
                <div class="completion-toggle">
                    <label class="toggle-container">
                        <input type="checkbox" id="complete_""" + str(lesson['id']) + """" 
                               class="toggle-input" 
                               """ + ("checked" if is_complete else "") + """
                               onchange="this.closest('.stCheckbox').querySelector('input[type=checkbox]').click()">
                        <div class="toggle-track">
                            <div class="toggle-indicator">
                                <div class="checkmark">
                                    <svg viewBox="0 0 24 24" id="ghq-svg-check" role="presentation" aria-hidden="true">
                                        <path d="M9.86 18a1 1 0 01-.73-.32l-4.86-5.17a1 1 0 111.46-1.37l4.12 4.39 8.41-9.2a1 1 0 111.48 1.34l-9.14 10a1 1 0 01-.73.33h-.01z"></path>
                                    </svg>
                                </div>
                            </div>
                        </div>
                        <div class="toggle-label">
                            <span class="toggle-label-text">
                                """ + ("Lição Concluída" if is_complete else "Marcar como Concluído") + """
                            </span>
                        </div>
                    </label>
                </div>
                """, unsafe_allow_html=True)
                
                # Adiciona o checkbox real do Streamlit (invisível)
                new_status = st.checkbox(
                    "Marcar como concluído",
                    value=is_complete,
                    key=f"complete_{lesson['id']}",
                    on_change=lambda: UserProgress.toggle_lesson_complete(lesson['id'], module_name),
                    label_visibility="collapsed"
                )
                
                # Atualiza o status se mudar
                if new_status != is_complete:
                    UserProgress.toggle_lesson_complete(lesson['id'], module_name)
                    st.rerun()
                
                # Adiciona estatísticas da lição
                st.markdown("""
                <div class="lesson-stats">
                    <div class="stat-item">
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                            <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
                            <circle cx="12" cy="12" r="3"></circle>
                        </svg>
                        <span>1.2k visualizações</span>
                    </div>
                    <div class="stat-item">
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                            <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"></path>
                        </svg>
                        <span>845 favoritos</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                # Botão para baixar material (se houver)
                doc_url = lesson.get('doc_url', '')
                if doc_url and pd.notna(doc_url) and str(doc_url).strip():
                    try:
                        doc_url = str(doc_url).strip()
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
                        
                        # Adiciona o script de cópia para área de transferência apenas uma vez
                        if 'copy_script_added' not in st.session_state:
                            st.markdown("""
                            <script>
                            function copyToClipboard(text, button) {
                                navigator.clipboard.writeText(text).then(() => {
                                    const originalHTML = button.innerHTML;
                                    button.innerHTML = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6L9 17l-5-5"/></svg><span>Copiado!</span>';
                                    
                                    setTimeout(() => {
                                        button.innerHTML = originalHTML;
                                    }, 2000);
                                }).catch(err => {
                                    console.error('Erro ao copiar texto: ', err);
                                });
                            }
                            </script>
                            <style>
                            .material-actions {
                                display: flex;
                                gap: 0.75rem;
                                flex-wrap: wrap;
                                margin: 1.5rem 0;
                            }
                            </style>
                            """, unsafe_allow_html=True)
                            st.session_state.copy_script_added = True
                            
                        # Gera os botões de ação
                        st.markdown(f"""
                        <div class="material-actions">
                            <a href="{download_url}" class="btn" download>
                                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                                    <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                                    <polyline points="7 10 12 15 17 10"></polyline>
                                    <line x1="12" y1="15" x2="12" y2="3"></line>
                                </svg>
                                <span>Baixar Material</span>
                            </a>
                            <a href="{view_url}" class="btn btn-outline" target="_blank" rel="noopener noreferrer">
                                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                                    <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
                                    <circle cx="12" cy="12" r="3"></circle>
                                </svg>
                                <span>Visualizar</span>
                            </a>
                            <button class="btn btn-icon" onclick="copyToClipboard('{view_url}', this)">
                                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                                    <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
                                    <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
                                </svg>
                                <span>Copiar Link</span>
                            </button>
                        </div>
                        
                        <div class="material-preview">
                            <div class="preview-header">
                                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                                    <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                                    <polyline points="14 2 14 8 20 8"></polyline>
                                    <line x1="16" y1="13" x2="8" y2="13"></line>
                                    <line x1="16" y1="17" x2="8" y2="17"></line>
                                    <polyline points="10 9 9 9 8 9"></polyline>
                                </svg>
                                <span>Pré-visualização do Material</span>
                            </div>
                            <div class="preview-content">
                                <h4>{lesson['title']}</h4>
                                <p>Clique em "Visualizar" para ver o conteúdo completo deste material de estudo.</p>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    except Exception as e:
                        st.warning("⚠️ Não foi possível carregar o material desta lição.")
                        print(f"Erro ao carregar material: {str(e)}")
        
        # Fecha a div do card da lição
        st.markdown("</div>", unsafe_allow_html=True)
        
    except Exception as e:
        st.error(f"Ocorreu um erro ao carregar a lição: {str(e)}")
        import traceback
        print(f"Erro em display_lesson: {traceback.format_exc()}")

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
