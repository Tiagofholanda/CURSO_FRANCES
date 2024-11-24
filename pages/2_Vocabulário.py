# pages/2_Vocabulário.py
import streamlit as st
from utils.quizzes import vocabulario_quiz
from utils.feedback import feedback_section

st.title("Vocabulário Básico")

st.write("""
### Expanda seu vocabulário em francês!

Aprenda novas palavras e expressões essenciais para se comunicar efetivamente.
""")

# Exibir o vídeo de Vocabulário via URL Bruta do GitHub
video_url = "https://raw.githubusercontent.com/seu_usuario/meu_site_frances/main/videos/vocabulario.mp4"  # Substitua pelo seu URL
st.video(video_url)

# Quiz de Vocabulário
vocabulario_quiz()

# Seção de Feedback
feedback_section()
