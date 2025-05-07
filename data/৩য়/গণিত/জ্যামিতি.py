import streamlit as st
from streamlit_drawable_canvas import st_canvas
from domain.services import AngleApproximator
from domain import BasePage


class GeometryPage(BasePage):
    def __init__(self):
        super().__init__(file_location=str(__file__))
        self.angle_approximator = AngleApproximator()

    def build_page(self, **args):
        col1, col2 = st.columns(2)
        with col1:
            canvas_result = st_canvas(
                drawing_mode="line",
                background_image=self.angle_approximator.get_angle_preview(),
            )
            st.write(canvas_result.json_data)
        with col2:
            st_canvas(
                initial_drawing=canvas_result.json_data,
                drawing_mode="point",
                background_image=self.angle_approximator.get_triangle_preview(),
            )


geometry = GeometryPage()
geometry.build_page()
