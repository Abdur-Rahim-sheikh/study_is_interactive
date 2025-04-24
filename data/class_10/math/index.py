from domain import Base
import streamlit as st

class Index(Base):
    def __init__(self):
        super().__init__("Index")

    def activate(self):
        st.write("১০ম শ্রেণির গণিত")


index = Index()
index.activate()