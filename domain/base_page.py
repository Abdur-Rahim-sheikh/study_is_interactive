from abc import ABC
from pathlib import Path

import streamlit as st
from streamlit.delta_generator import DeltaGenerator


class BasePage(ABC):
    def __init__(self, file_location: str, page_icon=None, menu_items: dict = {}):
        self.origin = Path(file_location)
        self.grade = self.origin.parents[1].stem
        self.chapter = self.origin.parent.stem
        self.topic = self.origin.stem

        self.header = f"{self.grade} শ্রেণির {self.chapter}"

        self.page_icon = page_icon
        self.menu_items = menu_items
        self.setup()

    def __hash__(self):
        return str(self.origin.absolute())

    def setup(self):
        st.set_page_config(
            page_title=self.header,
            page_icon=self.page_icon,
            layout="wide",
            menu_items=self.menu_items,
        )

        st.header(self.header)
        st.subheader(self.topic)
        # this might be later removed
        st.sidebar.header(self.header)

    def index_page(self, max_col=4):
        root = self.origin.parents[2]
        if root.name != "data":
            raise RuntimeError(f"page need to be inside `data` {root}")
        root = root.parent
        info = {
            path.stem: path.relative_to(root)
            for path in self.origin.parent.iterdir()
            if path.stem != self.topic
        }

        num_row = len(info) // max_col
        cols: list[DeltaGenerator] = []
        for _ in range(num_row):
            cols += st.columns(max_col)

        left = len(info) % max_col
        if left:
            cols += st.columns(left)

        for (name, url), col in zip(info.items(), cols):
            card = col.container(border=False)
            card.page_link(
                label=name, page=url, icon=":material/book_5:", use_container_width=True
            )
