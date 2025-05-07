from pathlib import Path

from PIL import Image


class AngleApproximator:
    """
    A class to convert st_canvas which is from streamlit_drawable_canvas
    it changes dictionary to help feedback loop to initial drawing or others
    It supports conversion between point, line, rect and circle
    polygon does not return any json, so it's no use here
    """

    def __init__(self, background_path="public/images/geometry_background"):
        self.background_path = Path(background_path)
        self.base_template = {
            "type": None,
            "version": None,
            "originX": None,
            "originY": None,
            "left": None,
            "top": None,
            "width": None,
            "height": None,
            "fill": None,
            "stroke": None,
            "strokeWidth": None,
            "strokeDashArray": None,
            "strokeLineCap": None,
            "strokeDashOffset": None,
            "strokeLineJoin": None,
            "strokeUniform": None,
            "strokeMiterLimit": None,
            "scaleX": None,
            "scaleY": None,
            "angle": None,
            "flipX": None,
            "flipY": None,
            "opacity": None,
            "shadow": None,
            "visible": None,
            "backgroundColor": None,
            "fillRule": None,
            "paintFirst": None,
            "globalCompositeOperation": None,
            "skewX": None,
            "skewY": None,
        }
        self.images = {}

    def __format_output(self, results: list):
        return {
            "version": self.canvas_version,
            "objects": results,
        }

    def __angle_preview(self, mode, graph_style=True):
        key = mode + "_graph" if graph_style else mode
        if key not in self.images:
            self.images[key] = Image.open(self.background_path / f"{key}.png")
        return self.images[key]

    def get_angle_preview(self, graph_style=True) -> Image:
        return self.__angle_preview("angle", graph_style=graph_style)

    def get_triangle_preview(self, graph_style=True) -> Image:
        return self.__angle_preview("triangle", graph_style=graph_style)

    def get_quadrangle_preview(self, graph_style=True) -> Image:
        return self.__angle_preview("quadrangle", graph_style=graph_style)

    @property
    def get_template(self, mode):
        if mode not in ["point", "line", "rect", "circle"]:
            raise ValueError(
                "Invalid mode. Choose from 'point', 'line', 'rect', or 'circle'."
            )

        base_template = self.base_template.copy()
        if mode in {"point", "circle"}:
            template = {
                **base_template,
                "radius": 20,
                "startAngle": 0,
                "endAngle": 6.283185307179586,
            }

        if mode == "line":
            template = {
                **base_template,
                "x1": None,
                "y1": None,
                "x2": None,
                "y2": None,
            }
        if mode == "rect":
            template = {
                **base_template,
                "rx": None,
                "ry": None,
            }

        return template
