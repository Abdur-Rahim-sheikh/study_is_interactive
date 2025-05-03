import math

import pandas as pd
import streamlit as st

from domain import BasePage
from domain.utils import to_roman
from itertools import accumulate


class StatisticsFrequencyDistribution(BasePage):
    def __init__(self):
        super().__init__(file_location=__file__)

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
            df = self.build_df(dist, diff=diff)
            st.dataframe(df, width=500)

    def __get_range(self, mn, mx, diff):
        # do this with yield
        for i in range(mn, mx + 1, diff):
            yield i, i + diff - 1

    def build_df(self, dist: list, diff=5):
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

        return df


sfd = StatisticsFrequencyDistribution()
sfd.build_page()
