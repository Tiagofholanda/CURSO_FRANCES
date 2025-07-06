"""
Módulo para gerenciar o cache de dados e o progresso do usuário.
"""
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import json
import hashlib

# Tempo de expiração do cache em segundos (1 hora)
CACHE_EXPIRATION = 3600

class DataCache:
    """Classe para gerenciar o cache de dados"""
    
    @staticmethod
    def get_cache_key(url: str) -> str:
        """Gera uma chave única para o cache baseada na URL"""
        return f"data_cache_{hashlib.md5(url.encode()).hexdigest()}"
    
    @staticmethod
    def get_cached_data(url: str):
        """Obtém dados do cache se ainda estiverem válidos"""
        cache_key = DataCache.get_cache_key(url)
        if cache_key in st.session_state:
            cache_data = st.session_state[cache_key]
            if datetime.now() < cache_data['expires_at']:
                return cache_data['data']
        return None
    
    @staticmethod
    def set_cached_data(url: str, data):
        """Armazena dados no cache"""
        cache_key = DataCache.get_cache_key(url)
        st.session_state[cache_key] = {
            'data': data,
            'expires_at': datetime.now() + timedelta(seconds=CACHE_EXPIRATION)
        }

class UserProgress:
    """Classe para gerenciar o progresso do usuário"""
    
    @staticmethod
    def get_progress_key() -> str:
        """Retorna a chave para armazenar o progresso do usuário"""
        if 'username' not in st.session_state:
            return "anonymous_progress"
        return f"user_progress_{st.session_state.username}"
    
    @staticmethod
    def get_progress() -> dict:
        """Obtém o progresso do usuário"""
        progress_key = UserProgress.get_progress_key()
        if progress_key not in st.session_state:
            # Tenta carregar do localStorage do navegador
            try:
                if 'progress' in st.session_state.get('_local_storage', {}):
                    st.session_state[progress_key] = st.session_state._local_storage['progress']
                else:
                    st.session_state[progress_key] = {
                        'completed_lessons': {},
                        'last_updated': datetime.now().isoformat()
                    }
            except:
                st.session_state[progress_key] = {
                    'completed_lessons': {},
                    'last_updated': datetime.now().isoformat()
                }
        return st.session_state[progress_key]
    
    @staticmethod
    def save_progress(progress: dict):
        """Salva o progresso do usuário"""
        progress_key = UserProgress.get_progress_key()
        progress['last_updated'] = datetime.now().isoformat()
        st.session_state[progress_key] = progress
        
        # Salva no localStorage do navegador
        try:
            st.markdown(
                f"""
                <script>
                if (window.localStorage) {{
                    localStorage.setItem('user_progress', JSON.stringify({json.dumps(progress)}));
                }}
                </script>
                """,
                unsafe_allow_html=True
            )
        except:
            pass
    
    @staticmethod
    def mark_lesson_complete(lesson_id: str, module_name: str):
        """Marca uma lição como concluída"""
        progress = UserProgress.get_progress()
        if 'completed_lessons' not in progress:
            progress['completed_lessons'] = {}
        
        if module_name not in progress['completed_lessons']:
            progress['completed_lessons'][module_name] = []
            
        if lesson_id not in progress['completed_lessons'][module_name]:
            progress['completed_lessons'][module_name].append(lesson_id)
            UserProgress.save_progress(progress)
    
    @staticmethod
    def is_lesson_complete(lesson_id: str, module_name: str) -> bool:
        """Verifica se uma lição foi concluída"""
        progress = UserProgress.get_progress()
        return (module_name in progress.get('completed_lessons', {}) and 
                lesson_id in progress['completed_lessons'][module_name])
    
    @staticmethod
    def get_module_progress(module_name: str, total_lessons: int) -> float:
        """Retorna o progresso do módulo como uma porcentagem"""
        if total_lessons == 0:
            return 0.0
            
        progress = UserProgress.get_progress()
        completed = len(progress.get('completed_lessons', {}).get(module_name, []))
        return min(100.0, (completed / total_lessons) * 100)
        
    @staticmethod
    def toggle_lesson_complete(lesson_id: str, module_name: str):
        """Alterna o status de conclusão de uma lição"""
        progress = UserProgress.get_progress()
        if 'completed_lessons' not in progress:
            progress['completed_lessons'] = {}
            
        if module_name not in progress['completed_lessons']:
            progress['completed_lessons'][module_name] = []
            
        if lesson_id in progress['completed_lessons'][module_name]:
            # Remove da lista de concluídos
            progress['completed_lessons'][module_name].remove(lesson_id)
        else:
            # Adiciona à lista de concluídos
            if lesson_id not in progress['completed_lessons'][module_name]:
                progress['completed_lessons'][module_name].append(lesson_id)
                
        # Salva as alterações
        UserProgress.save_progress(progress)

def load_cached_data(url: str, load_function):
    """Carrega dados do cache ou da fonte original se o cache estiver expirado"""
    # Tenta obter do cache
    cached_data = DataCache.get_cached_data(url)
    if cached_data is not None:
        return cached_data
    
    # Se não estiver em cache ou expirado, carrega os dados
    data = load_function()
    
    # Armazena no cache
    if data is not None:
        DataCache.set_cached_data(url, data)
    
    return data
