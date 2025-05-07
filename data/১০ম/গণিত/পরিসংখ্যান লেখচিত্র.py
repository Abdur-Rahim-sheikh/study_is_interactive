from itertools import accumulate

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
from domain.services import Animate
from domain import BasePage
from domain.utils import strToList
from matplotlib.axes import Axes


class StatisticsGraph(BasePage):
    AVAILABLE_COLUMNS = ["শ্রেণি ব্যবধান", "মধ্যমান", "গনসংখ্যা", "ক্রমযোজিত গনসংখ্যা"]

    def __init__(self):
        super().__init__(file_location=str(__file__))
        self.animate = Animate()

    def build_page(self, **args):
        freqs, starter, diff = self.take_input()
        df = self.build_df(freqs, starter, diff, ["শ্রেণি ব্যবধান", "গনসংখ্যা"])
        st.dataframe(df.T)
        if st.button("সমাধান দেখুন"):
            self.show_solution(freqs, starter, diff)

    def build_df(self, freqs, starter, diff, columns):
        if not all(col in self.AVAILABLE_COLUMNS for col in columns):
            st.error(
                "Invalid columns selected."
                f"{[col for col in columns if col not in self.AVAILABLE_COLUMNS]}"
            )
            return None
        df = pd.DataFrame()
        if "শ্রেণি ব্যবধান" in columns:
            df["শ্রেণি ব্যবধান"] = [
                f"{starter + i * diff} - {starter + (i + 1) * diff}"
                for i in range(len(freqs))
            ]
        if "মধ্যমান" in columns:
            df["মধ্যমান"] = [starter + diff * (2 * i + 1) / 2 for i in range(len(freqs))]
        if "গনসংখ্যা" in columns:
            df["গনসংখ্যা"] = freqs.copy()
        if "ক্রমযোজিত গনসংখ্যা" in columns:
            df["ক্রমযোজিত গনসংখ্যা"] = list(accumulate(freqs))
        return df

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

        return freqs, starter, diff

    def __attach_plt_attributes(self, ax: Axes, title, starter, diff, freqs):
        ax.set_title(title)
        ax.set_xticks(range(len(freqs) + 1))
        ax.set_xticklabels(
            [starter + i * diff for i in range(len(freqs) + 1)],
            rotation=45,
        )

    def show_solution(self, freqs, starter, diff):
        self.animate.write("প্রাপ্ত উপাত্ত থেকে সারণি তৈরি করা হবেঃ")
        df = self.build_df(freqs, starter, diff, self.AVAILABLE_COLUMNS)
        st.dataframe(df, width=600)

        col1, col2, col3 = st.columns(3)
        with col1:
            # aotolekh = graph
            self.animate.write("ছক কাগজের ")
            fig1, ax1 = plt.subplots()
            self.__attach_plt_attributes(ax1, "Histogram", starter, diff, freqs)
            ax1.bar(
                range(len(freqs)),
                freqs,
                width=1,
                edgecolor="black",
                align="edge",
                color="gray",
                alpha=0.7,
            )
            st.pyplot(fig1)
        with col2:
            # gonosongkhya = frequency polygon
            fig2, ax2 = plt.subplots()

            self.__attach_plt_attributes(ax2, "Frequency Polygon", starter, diff, freqs)
            ax2.plot(
                [0] + [idx + 0.5 for idx in range(len(freqs))] + [len(freqs)],
                [0] + freqs + [0],
                marker="o",
                linestyle="-",
                color="blue",
                alpha=0.7,
            )
            ax2.bar(
                range(len(freqs)),
                freqs,
                width=1,
                edgecolor="black",
                align="edge",
                color="gray",
                alpha=0.7,
            )
            st.pyplot(fig2)

        with col3:
            # ojiv rekha = Ogive Graph
            fig3, ax3 = plt.subplots()
            self.__attach_plt_attributes(ax3, "Ogive Curve", starter, diff, freqs)
            ax3.plot(
                range(len(freqs)),
                list(accumulate(freqs)),
                marker="o",
                linestyle="-",
                color="green",
                alpha=0.7,
            )
            st.pyplot(fig3)


sg = StatisticsGraph()
sg.build_page()
