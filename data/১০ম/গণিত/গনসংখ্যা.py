import base64
import math
import time
from io import BytesIO
from itertools import accumulate

import pandas as pd
import streamlit as st
from PIL import Image

from domain import BasePage
from domain.services import Animate
from domain.utils import strToList


class StatisticsFrequencyDistribution(BasePage):
    def __init__(self, tally_src="public/images"):
        super().__init__(file_location=str(__file__))
        self.animate = Animate()

        self.tally_images = self.__load_images(tally_src)

    @staticmethod
    @st.cache_data
    def __load_images(tally_src):
        tally_images = []
        empty = Image.new("RGBA", (20, 40), (255, 255, 255, 0))
        buffer = BytesIO()
        empty.save(buffer, format="PNG")
        base_64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
        tally_images.append(f"data:image/png;base64,{base_64}")
        for i in range(1, 6):
            img = Image.open(f"{tally_src}/tally_{i}.png").convert("RGBA")
            buffer = BytesIO()
            img.save(buffer, format="PNG")
            base_64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
            tally_images.append(f"data:image/png;base64,{base_64}")
        return tally_images

    def build_page(self):
        # fmt: off
        arr = [14,14,14,13,12,13,10,10,11,12,11,10,9,8,
            9,11,10,10,8,9,7,6,6,6,6,7,8,9,9,8,7,]
        # fmt: on
        col1, col2 = st.columns([3, 1], gap="large", vertical_alignment="bottom")
        with col1:
            dist = st.text_area(
                placeholder=",".join([str(i) for i in arr]),
                label="গনসংখ্যা মাণগুলি লেখি ",
                help="সংখ্যাগুলিকে কমা দিয়ে আলাদা কর 12,2,3,4,5",
            )
            dist = strToList(dist)
            if dist and min(dist) < 0:
                st.error("গনসংখ্যা ঋণাত্মক হতে পারবে না")
                st.stop()
        with col2:
            diff = st.number_input(label="শ্রেণি ব্যবধানঃ ", value=5, min_value=1)

        if len(dist) > 0 and st.button("গনসংখ্যা নিবেশন দেখি"):
            df, info = self.build_df(dist, diff=diff)
            self.show_info(info)
            time.sleep(0.5)
            self.animate.write(
                f"শ্রেণি ব্যবধান {info['diff']} নিয়ে উপাত্তসমূহ বিন্যাস করলে গনসংখ্যা / ঘটনসংখ্যা নিবেশন সারণি নিম্নরূপঃ "
            )
            time.sleep(1)
            st.dataframe(
                df,
                width=550,
                column_config={
                    "ট্যালি চিহ্ন": st.column_config.ImageColumn(
                        "ট্যালি চিহ্ন", help="গনসংখ্যা সমান মান ট্যালিতে দেখুন", width="medium"
                    )
                },
            )

    def show_info(self, info, interval=0.5):
        self.animate.write(
            f"উপাত্তের সবচেয়ে ছোট সংখ্যা {info['min']} এবং বড় সংখ্যা {info['max']}"
        )
        time.sleep(interval)
        dist_range = (info["max"] - info["min"]) + 1
        self.animate.write(
            f"সুতরাং উপাত্তের পরিসর = ({info['max']} - {info['min']}) + 1 = {dist_range}"
        )
        time.sleep(interval)
        sections = dist_range / info["diff"]
        sections_upper = math.ceil(sections)
        self.animate.write(
            f"এখন শ্রেণি ব্যবধান যদি {info['diff']} হয়,তাহলে শ্রেণি সংখ্যা হবে,"
        )
        time.sleep(interval)
        self.animate.latex(
            rf"\frac{{{dist_range}}}{{{info['diff']}}} = {sections:.2f}"
            rf"\Rightarrow  \lceil {sections:.2f} \rceil = {sections_upper}"
        )

    def __cumsum_annotate(self, df, row):
        if row.name == 0:
            return str(row["ক্রমযোজিত গনসংখ্যা"])
        return f"{row['গনসংখ্যা']} + {df.at[row.name - 1, 'ক্রমযোজিত গনসংখ্যা']} = {row['ক্রমযোজিত গনসংখ্যা']}"

    def __tally(self, num):
        if num == 0:
            return self.tally_images[0]  # empty image

        parts = []
        for i in range(num // 5):
            parts.append(self.tally_images[5])  # tally_5.png

        x = num % 5
        if x > 0:
            parts.append(self.tally_images[x])

        images = [
            Image.open(BytesIO(base64.b64decode(uri.split(",")[1]))) for uri in parts
        ]

        widths, heights = zip(*(img.size for img in images))
        total_width = sum(widths)
        max_height = max(heights)

        new_img = Image.new("RGBA", (total_width, max_height), (255, 255, 255, 0))
        x_offset = 0
        for img in images:
            new_img.paste(img, (x_offset, 0), img)
            x_offset += img.width

        buffer = BytesIO()
        new_img.save(buffer, format="PNG")
        return f"data:image/png;base64,{base64.b64encode(buffer.getvalue()).decode()}"

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
                "ট্যালি চিহ্ন": [self.__tally(num) for num in arr],
                "গনসংখ্যা": arr,
                "ক্রমযোজিত গনসংখ্যা": list(accumulate(arr)),
            }
        )

        if annote:
            df["ক্রমযোজিত গনসংখ্যা"] = df.apply(
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
# fmt: off
example_values = []

# fmt: on
md = """
    আমরা এখানে গনসংখ্যা নিবেশন সারণি অনুশীলন করবো।
    
    উদাহরন ১ঃ  কোন এক শীত মৌসুমে শ্রীমঙ্গলে জানুয়ারি মাসের ৩১ দিনের সর্বনিম্ম তাপমাত্রা ডিগ্রি সেলসিয়াসে দেওয়া হল।

    ```python
    14, 14, 13, 12, 13, 10, 10, 11, 12, 11, 10, 9, 8, 9, 11, 10, 10, 8,9, 7, 6, 6, 6, 6, 7, 8, 9, 9, 8, 7
    ```
    সর্বনিম্ম তাপমাত্রার গনসংখ্যা নিবেশন সারণি তৈরি করো। 

    এই অংকটি করার জন্য আমাদের আর একটা জিনিস দরকার, আর তা হল শ্রেণি ব্যবধান।
    এবার দেখ নিচের প্রথম টেক্সটবক্সে গনসংখ্যা গুলি কমা, কমা দিয়ে লিখে দাও, এবং ডান পাশের টেক্সটবক্সে শ্রেণি ব্যবধান লিখে দাও।
    তারপর `গনসংখ্যা নিবেশন দেখি` বাটনে ক্লিক করো।
    এবার সঠিক উত্তরটি তোমার খাতায় লেখা উত্তরের সাথে মিলাও। 

    """
sfd.info(md)
sfd.build_page()
