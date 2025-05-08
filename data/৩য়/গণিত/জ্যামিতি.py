import streamlit as st
from streamlit_drawable_canvas import st_canvas
from domain.services import AngleApproximator
from domain import BasePage


class GeometryPage(BasePage):
    def __init__(self):
        super().__init__(file_location=str(__file__))

        self.angle_approximator = AngleApproximator()

        self.stroke_width = st.sidebar.slider("Stroke width: ", 1, 25, 3)

        self.stroke_color = st.sidebar.color_picker("Stroke color hex: ")
        self.realtime_update = st.sidebar.checkbox("Update in realtime", True)

    def build_page(self, **args):
        tabs = st.tabs(["কোন", "ত্রিভুজ", "চতুর্ভুজ", "পরীক্ষা", "আঁকিবুঁকি"])
        with tabs[0]:
            self.angle()

    def angle(self):
        col1, col2 = st.columns(2)

        with col1:
            canvas_result = st_canvas(
                drawing_mode="line",
                background_image=self.angle_approximator.get_angle_preview(),
                stroke_width=self.stroke_width,
                stroke_color=self.stroke_color,
                update_streamlit=self.realtime_update,
            )

            st.write(canvas_result.json_data)
        with col2:
            points = self.__extract_points(canvas_result.json_data)

            approximation = self.angle_approximator.get_angle(points)
            if canvas_result.image_data is not None:
                st.image(canvas_result.image_data, caption="কোন প্রাকদর্শন")

    def __extract_points(self, json_data):
        if json_data is None or len(json_data["objects"]) > 2:
            st.stop()


geometry = GeometryPage()
geometry.build_page()
