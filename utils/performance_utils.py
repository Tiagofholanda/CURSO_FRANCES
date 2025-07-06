import streamlit as st
from functools import wraps
import time
import hashlib
import os
from typing import Callable, Any, Dict, List, Optional, Union
import pandas as pd

# Configuração do diretório de cache
CACHE_DIR = os.path.join(os.path.dirname(__file__), "..", ".cache")
os.makedirs(CACHE_DIR, exist_ok=True)

def memoize_with_ttl(ttl_seconds: int = 3600):
    """
    Decorator para armazenar em cache o resultado de uma função com tempo de vida.
    
    Args:
        ttl_seconds: Tempo de vida do cache em segundos (padrão: 1 hora)
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Gera uma chave única para esta chamada de função
            cache_key = f"{func.__name__}_{_generate_cache_key(args, kwargs)}"
            cache_file = os.path.join(CACHE_DIR, f"{cache_key}.pkl")
            
            # Verifica se o cache é válido
            if _is_cache_valid(cache_file, ttl_seconds):
                try:
                    return _load_from_cache(cache_file)
                except Exception as e:
                    st.warning(f"Erro ao carregar do cache: {e}")
            
            # Se o cache não for válido, executa a função
            result = func(*args, **kwargs)
            
            # Salva o resultado no cache
            try:
                _save_to_cache(result, cache_file)
            except Exception as e:
                st.warning(f"Erro ao salvar no cache: {e}")
            
            return result
        return wrapper
    return decorator

def _generate_cache_key(args: tuple, kwargs: dict) -> str:
    """Gera uma chave de cache única para os argumentos fornecidos."""
    key_parts = []
    
    # Adiciona argumentos posicionais
    for arg in args:
        if isinstance(arg, (str, int, float, bool, type(None))):
            key_parts.append(str(arg))
        elif hasattr(arg, '__dict__'):
            key_parts.append(str(arg.__dict__))
        else:
            key_parts.append(str(arg))
    
    # Adiciona argumentos nomeados
    for k, v in sorted(kwargs.items()):
        key_parts.append(f"{k}={v}")
    
    # Cria um hash da chave
    key_string = "_".join(key_parts)
    return hashlib.md5(key_string.encode()).hexdigest()

def _is_cache_valid(cache_file: str, ttl_seconds: int) -> bool:
    """Verifica se o cache é válido."""
    if not os.path.exists(cache_file):
        return False
    
    file_age = time.time() - os.path.getmtime(cache_file)
    return file_age < ttl_seconds

def _save_to_cache(data: Any, cache_file: str) -> None:
    """Salva dados no cache."""
    import pickle
    
    # Cria o diretório de cache se não existir
    os.makedirs(os.path.dirname(cache_file), exist_ok=True)
    
    # Salva os dados em um arquivo temporário primeiro
    temp_file = f"{cache_file}.tmp"
    with open(temp_file, 'wb') as f:
        if isinstance(data, pd.DataFrame):
            data.to_pickle(f, compression='gzip')
        else:
            pickle.dump(data, f, protocol=pickle.HIGHEST_PROTOCOL)
    
    # Substitui o arquivo antigo pelo novo
    if os.path.exists(cache_file):
        os.remove(cache_file)
    os.rename(temp_file, cache_file)

def _load_from_cache(cache_file: str) -> Any:
    """Carrega dados do cache."""
    import pickle
    
    with open(cache_file, 'rb') as f:
        # Tenta carregar como DataFrame primeiro
        try:
            import pandas as pd
            return pd.read_pickle(f, compression='gzip')
        except:
            f.seek(0)  # Volta para o início do arquivo
            return pickle.load(f)

def clear_cache() -> None:
    """Limpa todo o cache."""
    import shutil
    
    if os.path.exists(CACHE_DIR):
        shutil.rmtree(CACHE_DIR)
        os.makedirs(CACHE_DIR, exist_ok=True)
        return True
    return False

def get_cache_size() -> int:
    """Retorna o tamanho total do cache em bytes."""
    total_size = 0
    
    if os.path.exists(CACHE_DIR):
        for dirpath, _, filenames in os.walk(CACHE_DIR):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                total_size += os.path.getsize(fp)
    
    return total_size

# Decorador para funções que retornam DataFrames
cached_dataframe = memoize_with_ttl(ttl_seconds=3600)  # 1 hora de cache por padrão

# Decorador para funções que retornam strings
cached_text = memoize_with_ttl(ttl_seconds=1800)  # 30 minutos de cache por padrão

# Decorador para funções de processamento pesado
cached_computation = memoize_with_ttl(ttl_seconds=86400)  # 24 horas de cache por padrão
