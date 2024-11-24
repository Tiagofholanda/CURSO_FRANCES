# pages/1_Introdução.py
import streamlit as st
from utils.quizzes import introducao_quiz
from utils.feedback import feedback_section

st.title("Introdução ao Francês")

st.write("""
### Bem-vindo à sua jornada de aprendizado em francês!

Nesta seção, você aprenderá os conceitos básicos da língua francesa, incluindo saudações, apresentações e frases do dia a dia.
""")

# Exibir o vídeo de Introdução via URL Bruta do GitHub
video_url = "https://raw.githubusercontent.com/seu_usuario/meu_site_frances/main/videos/introducao.mp4"  # Substitua pelo seu URL
st.video(video_url)

# Quiz de Introdução
introducao_quiz()

# Seção de Feedback
feedback_section()
