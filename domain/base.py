import streamlit as st

class Base:
    def __init__(self, name: str):
        self.name = name

    def activate(self):
        st.write(f"Implementing {self.name} class")
