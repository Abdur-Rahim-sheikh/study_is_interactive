import pandas as pd
import streamlit as st

from domain import BasePage
from domain.utils import strToList


class StatisticsGraph(BasePage):
    def __init__(self):
        super().__init__(file_location=__file__)

    def build_page(self, **args):
        self.take_input()

    def take_input(self):
        col1, col2, col3 = st.columns([1, 1, 5])
        starter = 0.0
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
        with col3:
            freqs = st.text_input(
                label="গনসংখ্যাঃ", help="গনসংখ্যা লিখুন যেমনঃ ৫, ১০, ২০, ১৫, ১০"
            )
            freqs = strToList(freqs)

        df = pd.DataFrame(
            {
                "শ্রেণি": [
                    f"{starter + i * diff} - {starter + (i + 1) * diff}"
                    for i in range(len(freqs))
                ],
                "গনসংখ্যা": freqs,
            }
        )
        st.dataframe(df.T)


sg = StatisticsGraph()
sg.build_page()
