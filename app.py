# app.py
import streamlit as st

st.set_page_config(page_title="Aulas de Francês", layout="wide")

st.title("Bem-vindo às Aulas de Francês")
st.write("Aqui você encontrará diversas videoaulas para aprender francês de forma eficiente.")

st.write("""
## Navegação
Use a barra lateral para navegar entre as diferentes aulas:
- **Introdução**
- **Vocabulário**
- **Gramática**
- **Pronúncia**
""")

st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Flag_of_France.svg/2560px-Flag_of_France.svg.png", width=300)
