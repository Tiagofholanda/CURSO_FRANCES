import json
import os
from pathlib import Path
import streamlit as st

def get_progress_file_path():
    """Retorna o caminho do arquivo de progresso"""
    return os.path.join(str(Path.home()), ".french_course_progress.json")

def load_progress():
    """Carrega o progresso salvo do arquivo"""
    progress_file = get_progress_file_path()
    if os.path.exists(progress_file):
        try:
            with open(progress_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}
    return {}

def save_progress(module_id, lesson_id, completed):
    """Salva o progresso de uma lição"""
    progress = load_progress()
    
    # Inicializa o módulo se não existir
    if module_id not in progress:
        progress[module_id] = {}
    
    # Atualiza o status da lição
    progress[module_id][lesson_id] = completed
    
    # Salva no arquivo
    try:
        with open(get_progress_file_path(), 'w', encoding='utf-8') as f:
            json.dump(progress, f, ensure_ascii=False, indent=2)
        return True
    except IOError as e:
        st.error(f"Erro ao salvar o progresso: {e}")
        return False

def is_lesson_completed(module_id, lesson_id):
    """Verifica se uma lição foi marcada como concluída"""
    progress = load_progress()
    return progress.get(module_id, {}).get(lesson_id, False)

def get_completed_lessons(module_id):
    """Retorna um conjunto com os IDs das lições concluídas do módulo"""
    progress = load_progress()
    return {k for k, v in progress.get(module_id, {}).items() if v}

def get_module_progress(module_id, total_lessons):
    """Calcula o progresso do módulo (0 a 100)"""
    if total_lessons == 0:
        return 0
    completed = len(get_completed_lessons(module_id))
    return int((completed / total_lessons) * 100)
