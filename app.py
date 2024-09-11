import streamlit as st
import main  # Import main.py
import about  # Import about.py

# Set up the page title and layout
st.set_page_config(
    page_title="FUPRE Chatbot",
    page_icon="🤖",
    #layout="centered"
)

pg = st.navigation([
    st.Page("main.py", url_path='main.py', title="Chatbot", icon="🤖"),
    st.Page("about.py", url_path='about.py', title="About FUPRE", icon="🏫"),
])
pg.run()