# pages/2_Vocabulário.py
import streamlit as st
from utils.quizzes import vocabulario_quiz
from utils.feedback import feedback_section

st.title("Vocabulário Básico")

st.write("""
### Expanda seu vocabulário em francês!

Aprenda novas palavras e expressões essenciais para se comunicar efetivamente.
""")

# Exibir o vídeo de Vocabulário
video_path = "videos/vocabulario.mp4"
st.video(video_path)

# Quiz de Vocabulário
vocabulario_quiz()

# Seção de Feedback
feedback_section()
