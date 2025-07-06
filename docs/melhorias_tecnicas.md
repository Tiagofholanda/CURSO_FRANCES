# Melhorias Técnicas - Curso de Francês

Este documento descreve as melhorias técnicas implementadas no aplicativo Curso de Francês para melhorar o desempenho, acessibilidade e experiência do usuário.

## Índice

1. [Otimização de Desempenho](#otimização-de-desempenho)
2. [Responsividade Melhorada](#responsividade-melhorada)
3. [Acessibilidade](#acessibilidade)
4. [Estrutura do Projeto](#estrutura-do-projeto)
5. [Como Usar](#como-usar)
6. [Próximos Passos](#próximos-passos)

## Otimização de Desempenho

### Cache de Dados
- Implementação de um sistema de cache em disco para dados carregados de fontes externas (Google Sheets)
- Cache de resultados de funções pesadas usando decoradores
- Limpeza automática de cache expirado

### Carregamento Preguiçoso
- Carregamento lazy de imagens e vídeos para melhorar o tempo de carregamento inicial
- Suporte a miniaturas de vídeo para melhor experiência do usuário

### Otimização de Recursos
- Minimização de requisições HTTP
- Compressão de ativos estáticos
- Uso eficiente de memória

## Responsividade Melhorada

### Layout Adaptativo
- Design responsivo que se adapta a diferentes tamanhos de tela
- Grid system flexível para organização do conteúdo
- Ajustes específicos para dispositivos móveis

### Componentes Responsivos
- Players de vídeo que se adaptam ao tamanho da tela
- Tabelas e cards que se ajustam automaticamente
- Navegação otimizada para dispositivos touch

## Acessibilidade

### Navegação por Teclado
- Suporte a teclas de atalho para navegação
- Foco visível em elementos interativos
- Navegação sequencial lógica

### Leitores de Tela
- Atributos ARIA para melhor compatibilidade com leitores de tela
- Textos alternativos para imagens e elementos não textuais
- Estrutura de cabeçalhos semântica

### Contraste e Cores
- Esquema de cores com bom contraste para melhor legibilidade
- Suporte a modo escuro/claro
- Personalização de temas

## Estrutura do Projeto

```
curso_frances/
│
├── utils/
│   ├── __init__.py           # Exportação de funções úteis
│   ├── accessibility_utils.py # Utilidades de acessibilidade
│   ├── cache_utils.py        # Funções de cache
│   ├── lazy_loading.py       # Carregamento preguiçoso de mídia
│   ├── performance_utils.py  # Otimizações de desempenho
│   ├── responsive_utils.py   # Utilidades de responsividade
│   └── video_utils.py        # Gerenciamento de vídeos
│
├── pages/
│   ├── 00_Introdução.py
│   ├── 01_Vocabulário.py
│   ├── 02_Pronúncia.py
│   └── 03_Gramática.py
│
├── assets/
│   ├── css/
│   │   └── styles.css
│   └── js/
│       └── main.js
│
├── .env.example             # Exemplo de variáveis de ambiente
├── app.py                   # Aplicativo principal
├── requirements.txt         # Dependências
└── README.md                # Documentação
```

## Como Usar

### Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/curso-frances.git
   cd curso-frances
   ```

2. Crie um ambiente virtual (opcional, mas recomendado):
   ```bash
   python -m venv venv
   source venv/bin/activate  # No Windows: venv\Scripts\activate
   ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure as variáveis de ambiente:
   - Copie `.env.example` para `.env`
   - Preencha com suas credenciais do Google Cloud

### Executando o Aplicativo

```bash
streamlit run app.py
```

### Exemplo de Uso

```python
from utils import (
    # Acessibilidade
    init_accessibility,
    add_skip_link,
    
    # Performance
    cached_dataframe,
    
    # Responsividade
    init_responsive,
    responsive_columns,
    is_mobile,
    
    # Vídeos
    display_video,
    create_video_card
)

# Inicializa as configurações
init_accessibility()
init_responsive()

# Adiciona link para pular para o conteúdo principal
add_skip_link()

# Exemplo de uso de cache
@cached_dataframe(ttl=3600)  # Cache por 1 hora
def load_data():
    # Código para carregar dados
    pass

# Exemplo de layout responsivo
col1, col2 = responsive_columns([1, 1])

with col1:
    st.write("Coluna 1")

with col2:
    st.write("Coluna 2")

# Exemplo de player de vídeo
display_video("https://www.youtube.com/watch?v=...")
```

## Próximos Passos

- [ ] Implementar testes automatizados
- [ ] Adicionar mais opções de personalização
- [ ] Melhorar a documentação da API
- [ ] Otimizar ainda mais o desempenho
- [ ] Adicionar suporte a mais formatos de mídia

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues e enviar pull requests.

## Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para mais detalhes.
