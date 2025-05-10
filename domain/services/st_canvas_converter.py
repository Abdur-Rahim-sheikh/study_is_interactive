class StCanvasConverter:
    """
    streamlit `st_canvas` from streamlit_drawable_canvas is now
    archived not maintained by `andfanilo` anymore,
    this this is a class to convert it's json data to different format
    ie line to point, rect to line, circle to point etc
    """

    def __init__(self):
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

    def __format_output(self, version: str, results: list):
        return {
            "version": version,
            "objects": results,
        }

    def get_points_of_line(self, line: dict) -> tuple:
        "It expects the same dict a line object has in st_canvas"
        center_x = line["left"]
        center_y = line["top"]
        x1 = line["x1"] + center_x
        y1 = line["y1"] + center_y
        x2 = line["x2"] + center_x
        y2 = line["y2"] + center_y
        return (x1, y1), (x2, y2)

    def point_to_line(self, data: dict) -> dict:
        """
        Convert point JSON to line JSON.
        """
        version = data.get("version", "1.0")
        points = data.get("objects", [])
        if len(points) < 2:
            raise ValueError("At least two points are required to create a line.")

        results = []

        for idx in range(1, len(points)):
            start = points[idx - 1]
            end = points[idx]

            line = self.get_template("line")
            # line["x1"]

        return self.__format_output(version, results)

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
