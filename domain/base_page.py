import streamlit as st

from abc import ABC, abstractmethod
class BasePage(ABC):
    def __init__(self, page_name: str, page_icon = None, menu_items: dict = {}):
        self.page_name = page_name
        self.page_icon = page_icon
        self.menu_items = menu_items
        
        st.set_page_config(
            page_title=self.page_name,
            page_icon=self.page_icon,
            menu_items=self.menu_items
        )
