from domain import BasePage
import streamlit as st

class Index(BasePage):
    def __init__(self):
        super().__init__("Index")

    def activate(self):
        st.write("১০ম শ্রেণির গণিত")


index = Index()
index.activate()