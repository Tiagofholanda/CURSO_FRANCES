# pages/4_Pronúncia.py
import streamlit as st
from utils.quizzes import pronunciacao_quiz
from utils.feedback import feedback_section

st.title("Pronúncia em Francês")

st.write("""
### Aperfeiçoe sua pronúncia em francês!

Pratique os sons específicos do francês e melhore sua fluência e compreensão auditiva.
""")

# Exibir o vídeo de Pronúncia
video_path = "videos/pronunciacao.mp4"
st.video(video_path)

# Quiz de Pronúncia
pronunciacao_quiz()

# Seção de Feedback
feedback_section()
