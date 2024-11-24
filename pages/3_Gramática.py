# pages/3_Gramática.py
import streamlit as st
from utils.quizzes import gramatica_quiz
from utils.feedback import feedback_section

st.title("Gramática Francesa")

st.write("""
### Domine a gramática do francês!

Aprenda sobre tempos verbais, concordância, preposições e muito mais para estruturar suas frases corretamente.
""")

# Exibir o vídeo de Gramática
video_path = "videos/gramatica.mp4"
st.video(video_path)

# Quiz de Gramática
gramatica_quiz()

# Seção de Feedback
feedback_section()
