# pages/4_Pronúncia.py
import streamlit as st
from utils.quizzes import pronunciacao_quiz
from utils.feedback import feedback_section

st.title("Pronúncia em Francês")

st.write("""
### Aperfeiçoe sua pronúncia em francês!

Pratique os sons específicos do francês e melhore sua fluência e compreensão auditiva.
""")

# Exibir o vídeo de Pronúncia via URL Bruta do GitHub
video_url = "https://raw.githubusercontent.com/seu_usuario/meu_site_frances/main/videos/pronunciacao.mp4"  # Substitua pelo seu URL
st.video(video_url)

# Quiz de Pronúncia
pronunciacao_quiz()

# Seção de Feedback
feedback_section()
