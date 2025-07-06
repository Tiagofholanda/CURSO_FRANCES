import streamlit as st
import pandas as pd
import time
from functools import wraps
import hashlib
import os

# Configuração do diretório de cache
CACHE_DIR = ".cache"
if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)

def get_cache_key(func_name, *args, **kwargs):
    """Gera uma chave única para o cache baseada nos argumentos da função."""
    key_parts = [func_name] + list(args) + [f"{k}={v}" for k, v in sorted(kwargs.items())]
    key_string = "_".join(str(part) for part in key_parts)
    return hashlib.md5(key_string.encode()).hexdigest()

def cached_dataframe(ttl=3600):
    ""
    Decorador para armazenar em cache DataFrames retornados por funções.
    
    Args:
        ttl: Tempo de vida do cache em segundos (padrão: 1 hora)
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Gera uma chave única para este conjunto de argumentos
            cache_key = get_cache_key(func.__name__, *args, **kwargs)
            cache_file = os.path.join(CACHE_DIR, f"{cache_key}.pkl")
            
            # Verifica se o cache é válido
            if os.path.exists(cache_file):
                file_age = time.time() - os.path.getmtime(cache_file)
                if file_age < ttl:
                    try:
                        # Tenta carregar do cache
                        return pd.read_pickle(cache_file)
                    except:
                        # Se houver erro ao ler o cache, continua para recriá-lo
                        pass
            
            # Se não tiver cache ou estiver expirado, executa a função
            result = func(*args, **kwargs)
            
            # Salva o resultado no cache
            if isinstance(result, pd.DataFrame) and not result.empty:
                try:
                    result.to_pickle(cache_file)
                except:
                    # Se não conseguir salvar o cache, apenas continua
                    pass
            
            return result
        return wrapper
    return decorator

def clear_cache():
    """Limpa todos os arquivos de cache."""
    for filename in os.listdir(CACHE_DIR):
        file_path = os.path.join(CACHE_DIR, filename)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(f"Erro ao deletar {file_path}: {e}")

# Exemplo de uso:
# @cached_dataframe(ttl=3600)  # Cache por 1 hora
# def minha_funcao_pesada():
#     # Código que retorna um DataFrame
#     return pd.DataFrame(...)
