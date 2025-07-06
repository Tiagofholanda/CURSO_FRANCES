# utils/quizzes.py
import streamlit as st

def introducao_quiz():
    st.header("Quiz de Introdução")
    pergunta = st.radio("Qual a tradução de 'Bonjour'?", ("Olá", "Adeus", "Obrigado", "Por favor"))
    if st.button("Enviar (Introdução)"):
        if pergunta == "Olá":
            st.success("Correto!")
        else:
            st.error("Resposta Incorreta. A resposta correta é 'Olá'.")

def vocabulario_quiz():
    st.header("Quiz de Vocabulário")
    pergunta = st.radio("Como se diz 'Obrigado' em francês?", ("Merci", "S'il vous plaît", "Bonjour", "Au revoir"))
    if st.button("Enviar (Vocabulário)"):
        if pergunta == "Merci":
            st.success("Correto!")
        else:
            st.error("Resposta Incorreta. A resposta correta é 'Merci'.")

def gramatica_quiz():
    st.header("Quiz de Gramática")
    pergunta = st.radio("Qual é o artigo definido masculino singular em francês?", ("Le", "La", "Les", "L'"))
    if st.button("Enviar (Gramática)"):
        if pergunta == "Le":
            st.success("Correto!")
        else:
            st.error("Resposta Incorreta. A resposta correta é 'Le'.")

def pronunciacao_quiz():
    st.header("Quiz de Pronúncia")
    pergunta = st.radio("Como se pronuncia 'Merci' corretamente?", ("Mêrsí", "Mérci", "Mêrsi", "Mersí"))
    if st.button("Enviar (Pronúncia)"):
        if pergunta.lower() == "mérci":
            st.success("Correto!")
        else:
            st.error("Resposta Incorreta. A resposta correta é 'Mérci'.")
