import streamlit as st
from streamlit_drawable_canvas import st_canvas
from domain.services import AngleApproximator
from domain import BasePage
from domain.models import Point
from domain.services import Animate
from domain.services import StCanvasConverter


class GeometryPage(BasePage):
    def __init__(self):
        super().__init__(file_location=str(__file__))

        self.angle_approximator = AngleApproximator()
        self.animate = Animate()
        self.canvas_converter = StCanvasConverter()
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
            points = self.__extract_points_from_line(canvas_result.json_data)
            if len(points) != 4:
                st.stop()
            st.write(points)
            approximation = self.angle_approximator.get_angle_points(
                points[0], points[1], points[2], points[3]
            )
            if canvas_result.image_data is not None:
                self.animate.draw_angle(
                    approximation[0], approximation[1], approximation[2]
                )

    def __extract_points_from_line(self, json_data):
        if json_data is None or len(json_data["objects"]) > 2:
            return []
        points = []
        for obj in json_data["objects"]:
            if obj["type"] != "line":
                continue

            p1, p2 = self.canvas_converter.get_points_of_line(obj)
            points.append(Point(*p1))
            points.append(Point(*p2))
        return points


geometry = GeometryPage()
geometry.build_page()
