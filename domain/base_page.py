import streamlit as st

from abc import ABC, abstractmethod
class BasePage(ABC):
    def __init__(self, file_location: str, page_icon = None, menu_items: dict = {}):
        paths = file_location.split("/")
        self.grade = paths[-3]
        self.chapter = paths[-2]
        self.topic = ".".join(paths[-1].split(".")[:-1])

        self.header = f"{self.grade} শ্রেণির {self.chapter}"
        
        self.page_icon = page_icon
        self.menu_items = menu_items
        self.setup()

    def setup(self):
        st.set_page_config(
            page_title=self.header,
            page_icon=self.page_icon,
            layout="wide",
            menu_items=self.menu_items
        )

        st.header(self.header)
        st.subheader(self.topic)
        # this might be later removed
        st.sidebar.header(self.header)

    @abstractmethod
    def build_page(self, **args):
        raise NotImplementedError("build_page method must be implemented in the derived class")