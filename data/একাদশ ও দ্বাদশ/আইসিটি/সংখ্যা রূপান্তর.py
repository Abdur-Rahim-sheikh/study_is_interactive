from domain import BasePage
import streamlit as st


class NumberConversion(BasePage):
    def __init__(self):
        super().__init__(__file__, page_icon=":material/sync_alt:")

    def add_form(self):
        with st.form("number_conversion"):
            num1 = st.number_input("যেই নাম্বারটিকে কনভার্ট করতে চান")

    def build_page(self):
        form_info = self.add_form()


nc = NumberConversion()
