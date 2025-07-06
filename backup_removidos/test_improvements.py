"""
Script para testar as melhorias técnicas implementadas.

Este script testa as funcionalidades de cache, carregamento preguiçoso,
responsividade e acessibilidade implementadas no aplicativo.
"""
import sys
import os
import time
import unittest
from unittest.mock import patch, MagicMock

# Adiciona o diretório raiz ao path para importar os módulos
sys.path.insert(0, os.path.abspath('.'))

from utils import (
    # Acessibilidade
    init_accessibility,
    add_skip_link,
    
    # Performance
    memoize_with_ttl,
    cached_dataframe,
    clear_cache,
    get_cache_size,
    
    # Responsividade
    init_responsive,
    is_mobile,
    
    # Vídeos
    get_video_embed_url,
    display_video
)

class TestPerformanceImprovements(unittest.TestCase):
    """Testa as melhorias de desempenho."""
    
    def setUp(self):
        """Configuração inicial para os testes."""
        # Limpa o cache antes de cada teste
        clear_cache()
    
    def test_memoize_with_ttl(self):
        """Testa o decorador de cache com tempo de vida."""
        # Função de teste
        @memoize_with_ttl(ttl_seconds=1)  # Cache de 1 segundo
        def test_func(x):
            return x * 2
        
        # Primeira chamada - deve calcular
        start_time = time.time()
        result1 = test_func(5)
        elapsed1 = time.time() - start_time
        
        # Segunda chamada - deve usar o cache
        start_time = time.time()
        result2 = test_func(5)
        elapsed2 = time.time() - start_time
        
        # Verifica se o resultado está correto
        self.assertEqual(result1, 10)
        self.assertEqual(result2, 10)
        
        # A segunda chamada deve ser mais rápida (usando cache)
        self.assertLess(elapsed2, elapsed1)
        
        # Aguarda o cache expirar
        time.sleep(1.1)
        
        # Terceira chamada - deve calcular novamente
        start_time = time.time()
        result3 = test_func(5)
        elapsed3 = time.time() - start_time
        
        # Deve ser mais lenta que a chamada com cache
        self.assertGreater(elapsed3, elapsed2)
    
    def test_cached_dataframe(self):
        """Testa o cache de DataFrames."""
        import pandas as pd
        
        # Função de teste que retorna um DataFrame
        @cached_dataframe(ttl=1)  # Cache de 1 segundo
        def get_test_data(size=1000):
            return pd.DataFrame({
                'id': range(size),
                'value': [i * 2 for i in range(size)]
            })
        
        # Primeira chamada - deve calcular
        df1 = get_test_data()
        
        # Segunda chamada - deve usar o cache
        df2 = get_test_data()
        
        # Verifica se os DataFrames são iguais
        pd.testing.assert_frame_equal(df1, df2)
        
        # Verifica o tamanho do cache
        cache_size = get_cache_size()
        self.assertGreater(cache_size, 0)
        
        # Limpa o cache e verifica se foi limpo
        clear_cache()
        self.assertEqual(get_cache_size(), 0)


class TestAccessibility(unittest.TestCase):
    """Testa as melhorias de acessibilidade."""
    
    @patch('streamlit.markdown')
    def test_init_accessibility(self, mock_markdown):
        """Testa a inicialização das configurações de acessibilidade."""
        init_accessibility()
        
        # Verifica se o markdown foi chamado para adicionar os estilos
        self.assertTrue(mock_markdown.called)
        args, kwargs = mock_markdown.call_args
        self.assertIn('<style>', args[0])
        self.assertIn('accessibility', args[0].lower())
    
    @patch('streamlit.markdown')
    def test_add_skip_link(self, mock_markdown):
        """Testa a adição do link para pular para o conteúdo principal."""
        add_skip_link()
        
        # Verifica se o markdown foi chamado para adicionar o link
        self.assertTrue(mock_markdown.called)
        args, kwargs = mock_markdown.call_args
        self.assertIn('skip-link', args[0])
        self.assertIn('main-content', args[0])


class TestResponsiveness(unittest.TestCase):
    """Testa as melhorias de responsividade."""
    
    def test_is_mobile(self):
        """Testa a detecção de dispositivos móveis."""
        # Simula um user agent de dispositivo móvel
        with patch.dict('os.environ', {'HTTP_USER_AGENT': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X)'}):
            self.assertTrue(is_mobile())
        
        # Simula um user agent de desktop
        with patch.dict('os.environ', {'HTTP_USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}):
            self.assertFalse(is_mobile())


class TestVideoUtils(unittest.TestCase):
    """Testa as utilidades de vídeo."""
    
    def test_get_video_embed_url(self):
        """Testa a conversão de URLs de vídeo para URLs de incorporação."""
        # Teste com URL do YouTube
        youtube_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        embed_url = get_video_embed_url(youtube_url)
        self.assertIn('youtube.com/embed/', embed_url)
        self.assertIn('dQw4w9WgXcQ', embed_url)
        
        # Teste com URL do Vimeo
        vimeo_url = "https://vimeo.com/123456789"
        embed_url = get_video_embed_url(vimeo_url)
        self.assertIn('vimeo.com/video/', embed_url)
        
        # Teste com URL do Google Drive
        drive_url = "https://drive.google.com/file/d/ABC123XYZ/view"
        embed_url = get_video_embed_url(drive_url)
        self.assertIn('drive.google.com/file/d/ABC123XYZ/preview', embed_url)
        
        # Teste com URL não suportada
        unsupported_url = "https://example.com/video.mp4"
        self.assertEqual(get_video_embed_url(unsupported_url), unsupported_url)
    
    @patch('streamlit.components.v1.html')
    def test_display_video(self, mock_html):
        """Testa a exibição de vídeo."""
        # Teste com URL do YouTube
        youtube_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        display_video(youtube_url)
        
        # Verifica se a função de exibição de HTML foi chamada
        self.assertTrue(mock_html.called)
        args, kwargs = mock_html.call_args
        self.assertIn('iframe', args[0])
        self.assertIn('youtube.com/embed/', args[0])


if __name__ == '__main__':
    # Executa os testes
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
    
    # Limpa o cache após os testes
    clear_cache()
