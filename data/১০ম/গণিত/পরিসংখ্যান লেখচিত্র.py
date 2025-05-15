from itertools import accumulate

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
from matplotlib.axes import Axes

from domain import BasePage
from domain.services import Animate
from domain.utils import strToList


class StatisticsGraph(BasePage):
    AVAILABLE_COLUMNS = ["শ্রেণি ব্যবধান", "মধ্যমান", "গনসংখ্যা", "ক্রমযোজিত গনসংখ্যা"]

    def __init__(self):
        super().__init__(file_location=str(__file__))
        self.animate = Animate()

    def build_page(self, **args):
        freqs, starter, diff = self.take_input()
        df = self.build_df(freqs, starter, diff, ["শ্রেণি ব্যবধান", "গনসংখ্যা"])
        st.dataframe(df.T, use_container_width=True)
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

        starter = col1.number_input(
            label="শ্রেণি শুরু",
            min_value=0.0,
            value=0.0,
            step=0.5,
        )

        diff = col2.number_input(
            label="শ্রেণি ব্যবধানঃ ",
            value=5,
            min_value=1,
        )

        freqs = col3.text_input(
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
            with st.container(height=200):
                self.animate.write(
                    (
                        f"ছক কাগজের প্রতি ঘরকে {diff} একক ধরে, x-অক্ষ বরাবর শ্রেণি সীমা"
                        "এবং y-অক্ষ বরাবর গনসংখ্যা নিয়ে নিচের আয়তলেখ আঁকি"
                    )
                )
            fig1, ax1 = plt.subplots()
            self.__attach_plt_attributes(ax1, "Histogram", starter, diff, freqs)
            ax1.set_xlabel("x", loc="right", fontsize=16, fontweight="bold")
            ax1.set_ylabel("y", loc="top", fontsize=16, fontweight="bold", rotation=0)

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
            with st.container(height=200):
                self.animate.write(
                    (
                        f"ছক কাগজের প্রতি ঘরকে {diff} একক ধরে, x-অক্ষ বরাবর শ্রেণি সীমা "
                        "এবং y-অক্ষ বরাবর গনসংখ্যা নিয়ে নিচের আয়তলেখ আঁকি "
                        "এবার আয়তলেখের আয়তসমূহের ভূমির বিপরীত বাহুর মধ্যবিন্দু যা শ্রেণির মধ্যবিন্দু চিহ্নিত করি "
                        "এখন চিহ্নিত মধ্যবিন্দুসমূহ রেখাংশ দ্বারা সংযুক্ত করি। প্রথম শ্রেণির প্রান্তবিন্দু ও শেষ শ্রেণির প্রান্তবিন্দুদ্বয়কে "
                        "শ্রেণি ব্যবধান নির্দেশক x-অক্ষের সাথে সংযুক্ত করে গনসংখ্যা বহুভুজ অঙ্কন করা হল।"
                    )
                )
            fig2, ax2 = plt.subplots()

            self.__attach_plt_attributes(ax2, "Frequency Polygon", starter, diff, freqs)
            ax2.set_xlabel("x", loc="right", fontsize=16, fontweight="bold")
            ax2.set_ylabel("y", loc="top", fontsize=16, fontweight="bold", rotation=0)

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
            with st.container(height=200):
                self.animate.write(f"""
                    গনসংখ্যা নিবেশনের ক্রমযোজিত গনসংখ্যা সারণি ব্যবহার করে ছক কাগজের উভয় অক্ষে 
                    প্রতি {diff} ঘরকে এক একক ধরে প্রদত্ত উপাত্তের ক্রমযোজিত গনসংখ্যার অজিভ রেখা আকা হলো। 
                """)
            fig3, ax3 = plt.subplots()
            self.__attach_plt_attributes(ax3, "Ogive Curve", starter, diff, freqs)
            ax3.set_xlabel("x", loc="right", fontsize=16, fontweight="bold")
            ax3.set_ylabel("y", loc="top", fontsize=16, fontweight="bold", rotation=0)

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
msg = """
    পরিসংখ্যান লেখচিত্রের ব্যবহার যানতে নিচের বইয়ের উদাহরণ টি দেখি, 

    বই উদাহরণ ৩ঃ  আপনার কোন একটি স্কুলের ১০ম শ্রেণির ৬০ জন শিক্ষার্থির ওজনের গনসংখ্যা নিবেশন দেয়া আছে, 
    
    | ওজন (কিলোগ্রাম) | 45.5 - 50.5 | 50.5 - 55.5| 55.5 - 60.5 | 60.5 - 65.5| 65.5 - 70.5 |
    |---|---|---|---|---|---|
    | গনসংখ্যা (শিক্ষার্থি সংখ্যা) | 5 | 10 | 20 | 15 | 10| 

    আপনাকে এই তথ্য থেকে আয়তলেখ (Histogram), 
    বহুভুজ (Frequency Polygon) ও অজিভ রেখা (Ogive Curve) আঁকতে পারেন। 
    
    প্রকৃত পক্ষে আপনার এতগুলি তথ্যের ও দরকার নেই, আপনার যানতে হবে
    - `শ্রেণি শুরু` যেটা এখানে `45.5`, 
    - `শ্রেণি ব্যবধান` যেটা এখানে `5`
    - `গনসংখ্যার মান` গুলি। যা আমরা গনসংখ্যা বক্সে কমা কমা দিয়ে `5 , 10 , 20 , 15 , 10`এভাবে লিখতে পারি। 
    
    ব্যাস এতেই হয়ে গেল, যত বিচিত্র আর বড় বিন্যাস ই হোক না কেন আপনি উত্তর পেয়ে যাবেন। 
    সমাধান দেখুন ক্লিক করেই। তাই নিজে খাতায় করুন আর সঠিক কিনা ভুল যাচাই করে নিন। 
"""
sg.info(msg)
sg.build_page()
