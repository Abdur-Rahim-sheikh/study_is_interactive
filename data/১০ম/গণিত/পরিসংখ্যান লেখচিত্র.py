import pandas as pd
import streamlit as st

from domain import BasePage

if "frequencies" not in st.session_state:
    st.session_state.frequencies = []


class StatisticsGraph(BasePage):
    def __init__(self):
        super().__init__(file_location=__file__)

    def build_page(self, **args):
        self.take_input()

    def take_input(self):
        col1, col2, _ = st.columns([1, 1, 5])
        with col1:
            starter = st.number_input(
                label="শ্রেণি শুরু",
                min_value=0.0,
                value=0.0,
                step=0.5,
            )
        with col2:
            diff = st.number_input(
                label="শ্রেণি ব্যবধানঃ ",
                value=5,
                min_value=1,
            )

        if st.button("কলাম যুক্ত করুন"):
            current = (
                st.session_state.frequencies[-1]
                if st.session_state.frequencies
                else starter
            )
            st.session_state.frequencies.append([current, current + diff])

        st.dataframe(st.session_state.frequencies)


sg = StatisticsGraph()
sg.build_page()
