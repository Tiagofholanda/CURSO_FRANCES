"""
Aplicativo principal do Curso de Francês - Versão Atualizada

Este é o ponto de entrada principal para o aplicativo Curso de Francês,
com todas as melhorias técnicas implementadas.
"""
import streamlit as st
import os
import sys
from pathlib import Path

# Adiciona o diretório raiz ao path para importar os módulos
sys.path.insert(0, str(Path(__file__).parent.absolute()))

# Importações de utilitários
from utils import (
    # Acessibilidade
    init_accessibility,
    add_skip_link,
    
    # Performance
    cached_dataframe,
    clear_cache,
    
    # Responsividade
    init_responsive,
    responsive_columns,
    is_mobile,
    
    # Vídeos
    display_video,
    create_video_card
)

# Importa as configurações
from config import (
    APP_NAME,
    APP_DESCRIPTION,
    APP_VERSION,
    THEME,
    SOCIAL_MEDIA,
    CONTACT_EMAIL
)

# Inicializa as configurações de acessibilidade e responsividade
init_accessibility()
init_responsive()

# Configuração da página
st.set_page_config(
    page_title=APP_NAME,
    page_icon="🇫🇷",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Adiciona o CSS personalizado
def load_custom_css():
    """Carrega o CSS personalizado para o aplicativo."""
    st.markdown(
        f"""
        <style>
            /* Estilos base */
            :root {{
                --primary-color: {THEME['primary_color']};
                --primary-dark: {THEME['secondary_color']};
                --text-color: {THEME['text_color']};
                --background-color: {THEME['background_color']};
                --secondary-background: {THEME['secondary_background']};
                --border-radius: {THEME['border_radius']};
                --box-shadow: {THEME['box_shadow']};
                --font-family: {THEME['font']};
            }}
            
            /* Melhora a acessibilidade do foco */
            :focus {{
                outline: 3px solid var(--primary-color) !important;
                outline-offset: 2px;
            }}
            
            /* Estilos para o conteúdo principal */
            .main .block-container {{
                max-width: 1200px;
                padding: 2rem 1rem;
            }}
            
            /* Estilos para dispositivos móveis */
            @media (max-width: 768px) {{
                .main .block-container {{
                    padding: 1rem 0.5rem;
                }}
                
                h1 {{
                    font-size: 1.8rem !important;
                }}
                
                h2 {{
                    font-size: 1.5rem !important;
                }}
            }}
            
            /* Estilos para a barra lateral */
            .css-1d391kg, .css-1d391kg p {{
                font-size: 1rem !important;
            }}
            
            /* Melhora a aparência dos botões */
            .stButton > button {{
                border-radius: var(--border-radius);
                border: 1px solid var(--primary-color);
                background-color: var(--primary-color);
                color: white;
                font-weight: 500;
                transition: all 0.3s ease;
            }}
            
            .stButton > button:hover {{
                background-color: var(--primary-dark);
                border-color: var(--primary-dark);
                transform: translateY(-1px);
                box-shadow: var(--box-shadow);
            }}
            
            /* Estilos para os cards */
            .card {{
                border-radius: var(--border-radius);
                box-shadow: var(--box-shadow);
                padding: 1.5rem;
                margin-bottom: 1.5rem;
                background-color: var(--secondary-background);
                transition: all 0.3s ease;
            }}
            
            .card:hover {{
                transform: translateY(-2px);
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
            }}
            
            /* Melhora a acessibilidade dos links */
            a {{
                color: var(--primary-color);
                text-decoration: none;
            }}
            
            a:hover, a:focus {{
                text-decoration: underline;
            }}
            
            /* Estilos para tabelas */
            table.dataframe {{
                width: 100%;
                border-collapse: collapse;
                margin: 1rem 0;
                font-size: 0.9em;
                min-width: 400px;
                box-shadow: var(--box-shadow);
                border-radius: var(--border-radius);
                overflow: hidden;
            }}
            
            table.dataframe thead tr {{
                background-color: var(--primary-color);
                color: white;
                text-align: left;
                font-weight: bold;
            }}
            
            table.dataframe th,
            table.dataframe td {{
                padding: 12px 15px;
            }}
            
            table.dataframe tbody tr {
                border-bottom: 1px solid #dddddd;
            }
            
            table.dataframe tbody tr:nth-of-type(even) {
                background-color: #f3f3f3;
            }
            
            table.dataframe tbody tr:last-of-type {
                border-bottom: 2px solid var(--primary-color);
            }
            
            table.dataframe tbody tr.active-row {
                font-weight: bold;
                color: var(--primary-color);
            }
        </style>
        """,
        unsafe_allow_html=True
    )

# Carrega o CSS personalizado
load_custom_css()

def show_header():
    """Exibe o cabeçalho da página."""
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.image(
            "https://via.placeholder.com/150x100?text=Logo",
            width=150,
            use_column_width=False
        )
    
    with col2:
        st.title(APP_NAME)
        st.caption(APP_DESCRIPTION)
    
    st.markdown("---")

def show_sidebar():
    """Exibe a barra lateral com navegação."""
    st.sidebar.title("Menu")
    
    # Navegação principal
    st.sidebar.markdown("### Navegação")
    page = st.sidebar.radio(
        "",
        ["Início", "Aulas", "Exercícios", "Vocabulário", "Sobre"],
        label_visibility="collapsed"
    )
    
    # Seção de configurações
    st.sidebar.markdown("---")
    st.sidebar.markdown("### Configurações")
    
    # Tema
    theme = st.sidebar.selectbox(
        "Tema",
        ["Claro", "Escuro", "Alto Contraste"],
        index=0
    )
    
    # Tamanho da fonte
    font_size = st.sidebar.slider(
        "Tamanho da Fonte",
        min_value=12,
        max_value=24,
        value=16,
        step=1
    )
    
    # Botão para limpar o cache
    if st.sidebar.button("🔄 Limpar Cache"):
        if clear_cache():
            st.sidebar.success("✅ Cache limpo com sucesso!")
            st.rerun()
        else:
            st.sidebar.error("❌ Erro ao limpar o cache.")
    
    # Rodapé da barra lateral
    st.sidebar.markdown("---")
    st.sidebar.markdown(
        f"""
        <div style="text-align: center;">
            <p>Versão {APP_VERSION}</p>
            <p>© 2023 {APP_NAME}</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    return page

def show_home():
    """Exibe a página inicial."""
    st.header("Bem-vindo ao Curso de Francês!")
    
    st.markdown("""
    Aprenda francês de forma interativa e divertida com nosso curso online.
    Navegue pelo menu lateral para acessar as lições, exercícios e muito mais.
    """)
    
    # Seção de destaques
    st.markdown("### Destaques")
    
    # Cria cards responsivos
    col1, col2 = responsive_columns([1, 1])
    
    with col1:
        with st.container():
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown("#### Aulas Interativas")
            st.markdown("Aprenda com vídeos, áudios e exercícios práticos.")
            if st.button("Começar a Aprender", key="start_learning"):
                st.session_state.page = "Aulas"
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        with st.container():
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown("#### Pratique o Vocabulário")
            st.markdown("Amplie seu vocabulário com nossas listas interativas.")
            if st.button("Ver Vocabulário", key="view_vocabulary"):
                st.session_state.page = "Vocabulário"
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)
    
    # Seção de vídeo de boas-vindas
    st.markdown("### Assista à Nossa Aula Introdutória")
    
    # Exemplo de vídeo com carregamento preguiçoso
    display_video(
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        width=0,  # Largura responsiva
        height=0,  # Altura proporcional
        autoplay=False,
        controls=True,
        lazy=True
    )

def show_lessons():
    """Exibe a página de aulas."""
    st.header("Aulas")
    
    # Lista de aulas disponíveis
    lessons = [
        {
            "title": "Introdução ao Francês",
            "description": "Aprenda as saudações básicas e apresentações em francês.",
            "duration": "15 min",
            "level": "Iniciante",
            "video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        },
        {
            "title": "Pronúncia Básica",
            "description": "Domine a pronúncia correta das vogais e consoantes francesas.",
            "duration": "20 min",
            "level": "Iniciante",
            "video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        },
        {
            "title": "Verbos no Presente",
            "description": "Aprenda a conjugar verbos regulares no presente do indicativo.",
            "duration": "25 min",
            "level": "Básico",
            "video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        },
        {
            "title": "Vocabulário: Comida e Bebida",
            "description": "Amplie seu vocabulário com palavras relacionadas a alimentos.",
            "duration": "20 min",
            "level": "Básico",
            "video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        }
    ]
    
    # Filtros
    st.markdown("### Filtros")
    
    col1, col2 = st.columns(2)
    
    with col1:
        level_filter = st.selectbox(
            "Nível",
            ["Todos"] + sorted(list(set(lesson["level"] for lesson in lessons)))
        )
    
    with col2:
        duration_filter = st.selectbox(
            "Duração",
            ["Todas", "Até 15 min", "15-30 min", "Acima de 30 min"]
        )
    
    # Aplica os filtros
    filtered_lessons = lessons
    
    if level_filter != "Todos":
        filtered_lessons = [l for l in filtered_lessons if l["level"] == level_filter]
    
    if duration_filter == "Até 15 min":
        filtered_lessons = [l for l in filtered_lessons if int(l["duration"].split()[0]) <= 15]
    elif duration_filter == "15-30 min":
        filtered_lessons = [l for l in filtered_lessons if 15 < int(l["duration"].split()[0]) <= 30]
    elif duration_filter == "Acima de 30 min":
        filtered_lessons = [l for l in filtered_lessons if int(l["duration"].split()[0]) > 30]
    
    # Exibe as aulas filtradas
    st.markdown(f"### {len(filtered_lessons)} Aulas Encontradas")
    
    for i, lesson in enumerate(filtered_lessons, 1):
        with st.container():
            st.markdown(f"<div class='card'>", unsafe_allow_html=True)
            
            # Cabeçalho do card
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(f"#### {i}. {lesson['title']}")
                st.caption(f"📚 {lesson['level']} • ⏱️ {lesson['duration']}")
                st.markdown(lesson["description"])
                
                # Botão para assistir a aula
                if st.button(f"Assistir Aula {i}", key=f"watch_lesson_{i}"):
                    st.session_state.current_lesson = lesson
                    st.session_state.show_lesson = True
                    st.rerun()
            
            with col2:
                # Miniatura do vídeo
                st.video(lesson["video_url"])
            
            st.markdown("</div>", unsafe_allow_html=True)

def show_vocabulary():
    """Exibe a página de vocabulário."""
    st.header("Vocabulário")
    
    # Categorias de vocabulário
    categories = [
        {
            "name": "Saudações",
            "words": ["Bonjour", "Salut", "Bonsoir", "Au revoir", "À bientôt"],
            "translations": ["Olá", "Oi", "Boa noite", "Adeus", "Até logo"],
            "icon": "👋"
        },
        {
            "name": "Números",
            "words": ["Un", "Deux", "Trois", "Quatre", "Cinq"],
            "translations": ["Um", "Dois", "Três", "Quatro", "Cinco"],
            "icon": "🔢"
        },
        {
            "name": "Cores",
            "words": ["Rouge", "Bleu", "Vert", "Jaune", "Noir"],
            "translations": ["Vermelho", "Azul", "Verde", "Amarelo", "Preto"],
            "icon": "🎨"
        },
        {
            "name": "Comida",
            "words": ["Pain", "Fromage", "Pomme", "Eau", "Vin"],
            "translations": ["Pão", "Queijo", "Maçã", "Água", "Vinho"],
            "icon": "🍎"
        }
    ]
    
    # Seletor de categorias
    category_names = [f"{cat['icon']} {cat['name']}" for cat in categories]
    selected_category = st.selectbox(
        "Selecione uma categoria:",
        category_names,
        index=0
    )
    
    # Encontra a categoria selecionada
    selected_index = category_names.index(selected_category)
    category = categories[selected_index]
    
    # Exibe o vocabulário da categoria selecionada
    st.markdown(f"### {category['icon']} {category['name']}")
    
    # Cria uma tabela com as palavras e traduções
    import pandas as pd
    
    df = pd.DataFrame({
        "Francês": category["words"],
        "Português": category["translations"]
    })
    
    # Estiliza a tabela
    def highlight_row(row):
        return ['background-color: #f0f2f6'] * len(row)
    
    st.dataframe(
        df.style.apply(highlight_row, axis=1),
        use_container_width=True,
        hide_index=True
    )
    
    # Adiciona um player de áudio para cada palavra
    st.markdown("### Pronúncia")
    
    for i, (word, translation) in enumerate(zip(category["words"], category["translations"]), 1):
        st.markdown(f"**{word}** - {translation}")
        
        # Botão para ouvir a pronúncia (simulado)
        if st.button(f"🔊 Ouvir pronúncia {i}", key=f"pronounce_{word}"):
            st.audio(f"https://www.soundoftext.com/voice?voice=fr-FR-Standard-A&text={word}")

def show_about():
    """Exibe a página sobre."""
    st.header("Sobre o Curso de Francês")
    
    st.markdown("""
    Bem-vindo ao Curso de Francês, uma plataforma interativa para aprender francês de 
    forma eficaz e divertida. Nosso objetivo é tornar o aprendizado de francês acessível 
    a todos, independentemente do seu nível de conhecimento.
    """)
    
    # Seção de recursos
    st.markdown("### Recursos do Curso")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        - 📚 Aulas interativas
        - 🎥 Vídeos com nativos
        - 🎧 Pronúncia autêntica
        - 📝 Exercícios práticos
        """)
    
    with col2:
        st.markdown("""
        - 🎯 Objetivos claros
        - 📈 Acompanhamento de progresso
        - 🏆 Certificado de conclusão
        - 📱 Acesso em qualquer dispositivo
        """)
    
    # Seção de depoimentos
    st.markdown("### O que nossos alunos dizem")
    
    testimonials = [
        {
            "name": "Ana Silva",
            "testimonial": "Aprendi mais em um mês do que em anos de curso presencial. Recomendo muito!",
            "rating": "⭐️⭐️⭐️⭐️⭐️"
        },
        {
            "name": "Carlos Oliveira",
            "testimonial": "A metodologia é excelente e os professores são muito atenciosos.",
            "rating": "⭐️⭐️⭐️⭐️⭐️"
        },
        {
            "name": "Mariana Santos",
            "testimonial": "Finalmente consegui me comunicar em francês na minha viagem para Paris. Obrigada!",
            "rating": "⭐️⭐️⭐️⭐️⭐️"
        }
    ]
    
    # Exibe os depoimentos em colunas
    cols = st.columns(len(testimonials))
    
    for i, testimonial in enumerate(testimonials):
        with cols[i]:
            with st.container():
                st.markdown(f"<div class='card'>", unsafe_allow_html=True)
                st.markdown(f"**{testimonial['name']}**")
                st.markdown(f"{testimonial['rating']}")
                st.markdown(f"*\"{testimonial['testimonial']}\"*")
                st.markdown("</div>", unsafe_allow_html=True)
    
    # Seção de contato
    st.markdown("### Entre em Contato")
    
    contact_form = """
    <form action="https://formsubmit.co/your@email.com" method="POST">
        <input type="hidden" name="_captcha" value="false">
        <input type="text" name="name" placeholder="Seu nome" required>
        <input type="email" name="email" placeholder="Seu email" required>
        <textarea name="message" placeholder="Sua mensagem"></textarea>
        <button type="submit">Enviar</button>
    </form>
    """
    
    st.markdown(contact_form, unsafe_allow_html=True)
    
    # Estilo para o formulário de contato
    st.markdown("""
    <style>
        input[type=text], input[type=email], textarea {
            width: 100%;
            padding: 12px;
            border: 1px solid #ccc;
            border-radius: 4px;
            box-sizing: border-box;
            margin-top: 6px;
            margin-bottom: 16px;
            resize: vertical;
            font-family: inherit;
        }
        
        button[type=submit] {
            background-color: #1E88E5;
            color: white;
            padding: 12px 20px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-weight: bold;
        }
        
        button[type=submit]:hover {
            background-color: #1565C0;
        }
        
        .contact-container {
            border-radius: 5px;
            background-color: #f2f2f2;
            padding: 20px;
        }
    </style>
    """, unsafe_allow_html=True)

def show_footer():
    """Exibe o rodapé da página."""
    st.markdown("---")
    
    # Links do rodapé
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### Links Rápidos")
        st.markdown("""
        - [Início](#)
        - [Aulas](#)
        - [Exercícios](#)
        - [Vocabulário](#)
        - [Sobre](#)
        """)
    
    with col2:
        st.markdown("### Redes Sociais")
        st.markdown("""
        - [Facebook](#)
        - [Twitter](#)
        - [Instagram](#)
        - [YouTube](#)
        - [LinkedIn](#)
        """)
    
    with col3:
        st.markdown("### Contato")
        st.markdown(f"""
        ✉️ {CONTACT_EMAIL}
        
        📞 (11) 1234-5678
        
        📍 São Paulo, SP - Brasil
        """)
    
    # Direitos autorais
    st.markdown("---")
    st.markdown(
        f"""
        <div style="text-align: center; color: #666;">
            <p>© 2023 {APP_NAME}. Todos os direitos reservados.</p>
            <p>Versão {APP_VERSION}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

def main():
    """Função principal do aplicativo."""
    # Inicializa a sessão para armazenar o estado da página
    if "page" not in st.session_state:
        st.session_state.page = "Início"
    
    # Exibe o cabeçalho
    show_header()
    
    # Exibe a barra lateral e obtém a página atual
    current_page = show_sidebar()
    
    # Atualiza a página com base na seleção do usuário
    if current_page == "Início":
        show_home()
    elif current_page == "Aulas":
        show_lessons()
    elif current_page == "Exercícios":
        st.header("Exercícios")
        st.info("🚧 Página em construção. Em breve teremos exercícios interativos!")
    elif current_page == "Vocabulário":
        show_vocabulary()
    elif current_page == "Sobre":
        show_about()
    
    # Exibe o rodapé
    show_footer()
    
    # Adiciona o link para pular para o conteúdo principal
    add_skip_link()

if __name__ == "__main__":
    main()
