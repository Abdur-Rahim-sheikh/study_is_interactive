import math
import time
from itertools import accumulate

import pandas as pd
import streamlit as st

from domain import BasePage
from domain.services import Animate
from domain.utils import to_roman


class StatisticsFrequencyDistribution(BasePage):
    def __init__(self):
        super().__init__(file_location=__file__)
        self.animate = Animate()

    def parse_integer(self, value, sep=","):
        value = value.strip().strip(",")
        if not value:
            return []
        try:
            return [int(i) for i in value.split(sep)]
        except ValueError:
            st.error(f"Invalid input. Please enter integers separated by ({sep}).")

    def build_page(self, **args):
        """
        if passed "annotate_cumulative_sum" as True,
        it will annotate how cumulative sum is calculated
        """
        # fmt: off
        arr = [14,14,14,13,12,13,10,10,11,12,11,10,9,8,
            9,11,10,10,8,9,7,6,6,6,6,7,8,9,9,8,7,]
        # fmt: on
        col1, col2 = st.columns([3, 1], gap="large", vertical_alignment="bottom")
        with col1:
            dist = st.text_area(
                value=",".join([str(i) for i in arr]),
                label="Enter the frequency distribution",
                help="comma separated: 1,2,3,4,5",
            )
            dist = self.parse_integer(dist)
        with col2:
            diff = st.number_input(label="শ্রেণি ব্যবধানঃ ", value=5, min_value=1)

        if len(dist) > 0 and st.button("See frequency distribution"):
            df, info = self.build_df(dist, diff=diff)
            self.show_info(info)
            time.sleep(0.5)
            self.animate.write(
                f"শ্রেণি ব্যবধান {info['diff']} নিয়ে উপাত্তসমূহ বিন্যাস করলে গনসংখ্যা / ঘটনসংখ্যা নিবেশন সারণি নিম্নরূপঃ "
            )
            time.sleep(1)
            st.dataframe(df, width=550)

    def show_info(self, info, interval=0.5):
        self.animate.write(
            f"উপাত্তের সবচেয়ে ছোট সংখ্যা {info['min']} এবং বড় সংখ্যা {info['max']}।"
        )
        time.sleep(interval)
        dist_range = (info["max"] - info["min"]) + 1
        self.animate.write(
            f"সুতরাং উপাত্তের পরিসর = ({info['max']} - {info['min']}) + 1 = {dist_range}।"
        )
        time.sleep(interval)
        sections = dist_range / info["diff"]
        sections_upper = math.ceil(sections)
        self.animate.write(
            f"এখন শ্রেণি ব্যবধান যদি {info['diff']} হয়, তাহলে শ্রেণি সংখ্যা হবে {dist_range} / {info['diff']} = {sections} = {sections_upper}।"
        )

    def __cumsum_annotate(self, df, row):
        if row.name == 0:
            return str(row["ক্রমযোজিত গনসংখ্যা"])
        return f"{row['গনসংখ্যা']} + {df.at[row.name - 1, 'ক্রমযোজিত গনসংখ্যা']} = {row['ক্রমযোজিত গনসংখ্যা']}"

    def build_df(self, dist: list, diff=5, annote=True):
        dist.sort()
        mn, mx = dist[0], dist[-1]
        dist_range = (mx - mn) + 1

        sections = dist_range / diff
        sections_uppper = math.ceil(sections)
        arr = [0] * sections_uppper
        lastIdx = 0
        secIdx = 0
        for i in range(mn, mx + 1, diff):
            cnt = 0
            while lastIdx < len(dist) and dist[lastIdx] < i + diff:
                cnt += 1
                lastIdx += 1
            arr[secIdx] = cnt
            secIdx += 1

        range_list = list(f"{x} - {y}" for x, y in self.__get_range(mn, mx, diff))

        df = pd.DataFrame(
            {
                "সীমা": range_list,
                "ট্যালি চিহ্ন": [to_roman(i) if i else "--" for i in arr],
                "গনসংখ্যা": arr,
                "ক্রমযোজিত গনসংখ্যা": list(accumulate(arr)),
            }
        )

        if annote:
            df["ক্ররমযোজিত গনসংখ্যা"] = df.apply(
                lambda row: self.__cumsum_annotate(df, row), axis=1
            )

        info = {
            "min": mn,
            "max": mx,
            "diff": diff,
        }
        return df, info

    def __get_range(self, mn, mx, diff):
        # do this with yield
        for i in range(mn, mx + 1, diff):
            yield i, i + diff - 1


sfd = StatisticsFrequencyDistribution()
sfd.build_page()
