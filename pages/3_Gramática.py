# pages/3_Gramática.py
import streamlit as st
from utils.quizzes import gramatica_quiz
from utils.feedback import feedback_section

st.title("Gramática Francesa")

st.write("""
### Domine a gramática do francês!

Aprenda sobre tempos verbais, concordância, preposições e muito mais para estruturar suas frases corretamente.
""")

# Exibir o vídeo de Gramática via URL Bruta do GitHub
video_url = "https://raw.githubusercontent.com/seu_usuario/meu_site_frances/main/videos/gramatica.mp4"  # Substitua pelo seu URL
st.video(video_url)

# Quiz de Gramática
gramatica_quiz()

# Seção de Feedback
feedback_section()
