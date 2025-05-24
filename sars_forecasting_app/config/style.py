def inject_style():
    import streamlit as st
    st.markdown("""
        <style>
        body {
            background-color: #1e1e1e;
            color: white;
        }
        .stButton>button {
            background-color: #00c3ff;
            color: white;
        }
        </style>
    """, unsafe_allow_html=True)