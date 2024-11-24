# utils/feedback.py
import streamlit as st
import os

def feedback_section():
    st.header("Deixe seu Feedback")
    feedback = st.text_area("Comentário:")
    if st.button("Enviar Feedback"):
        if feedback:
            # Salvar feedback em um arquivo de texto
            with open("feedback.txt", "a", encoding="utf-8") as f:
                f.write(feedback + "\n")
            st.success("Obrigado pelo seu feedback!")
        else:
            st.warning("Por favor, deixe um comentário antes de enviar.")
