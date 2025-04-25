from domain import BasePage
import streamlit as st

class Index(BasePage):
    def __init__(self):
        super().__init__(file_location=__file__)
    def activate(self):
        st.write("Hello kacher manus?")


index = Index()
index.activate()