import streamlit as st
from main import md_main

st.set_page_config(
    page_title="Custos do Intercâmbio",
    layout="wide",
    page_icon="assets/appicon.png",
    initial_sidebar_state='expanded'
)

st.markdown(
        """
        <style>
        .main {
        width: 85%;
        max-width: 85%;
        }
        </style>
        """,
        unsafe_allow_html=True
    )


st.sidebar.image("assets/appicon.png")
md_main()