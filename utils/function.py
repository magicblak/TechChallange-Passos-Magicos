import streamlit as st

def create_title(text):
    st.markdown(f'<h1 style="color: #fbba00;">{text}</h1>', unsafe_allow_html=True)
def create_section_title(text):
    st.markdown(f'<h1 style="color: #ed3237;">{text}</h1>', unsafe_allow_html=True)