class stCanvasDictConverter:
    """
    A class to convert st_canvas which is from streamlit_drawable_canvas
    it changes dictionary to help feedback loop to initial drawing or others
    It supports conversion between point, line, rect and circle
    polygon does not return any json, so it's no use here
    """

    def __init__(self, canvas_version):
        self.canvas_version = canvas_version
        self.base_template = {
            "type": None,
            "version": self.canvas_version,
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

    def __format_output(self, results: list):
        return {
            "version": self.canvas_version,
            "objects": results,
        }

    def point_to_line(self, points: list) -> dict:
        """
        Convert point JSON to line JSON.
        """
        if len(points) < 2:
            raise ValueError("At least two points are required to create a line.")

        results = []

        for idx in range(1, len(points)):
            start = points[idx - 1]
            end = points[idx]

            line = self.get_template("line")
            # line["x1"]

        return self.__format_output(results)

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
