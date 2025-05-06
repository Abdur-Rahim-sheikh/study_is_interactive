import streamlit as st
from streamlit_drawable_canvas import st_canvas

from domain import BasePage


class GeometryPage(BasePage):
    def __init__(self):
        super().__init__(__file__)

    def build_page(self, **args):
        col1, col2 = st.columns(2)
        with col1:
            canvas_result = st_canvas(drawing_mode="line")
            st.write(canvas_result.json_data)
        with col2:
            st_canvas(initial_drawing=canvas_result.json_data, drawing_mode="point")


geometry = GeometryPage()
geometry.build_page()
