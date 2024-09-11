import streamlit as st
import main  # Import main.py
import about  # Import about.py

pg = st.navigation([
    st.Page("main.py", url_path='main.py', title="Chatbot", icon="🤖"),
    st.Page("about.py", url_path='about.py', title="About FUPRE", icon="🏫"),
])
pg.run()