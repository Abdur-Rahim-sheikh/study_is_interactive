import time

import streamlit as st
from PIL import Image, ImageDraw

from ..models import Point


class Animate:
    BASE_COLORS = [
        "#000000",  # Black
        "#e6194b",  # Red
        "#3cb44b",  # Green
        "#ffe119",  # Yellow
        "#0082c8",  # Blue
        "#f58231",  # Orange
        "#911eb4",  # Purple
        "#46f0f0",  # Cyan
        "#f032e6",  # Pink
        "#d2f53c",  # Lime
        "#fabebe",  # Light Pink
        "#008080",  # Teal
        "#e6beff",  # Lavender
        "#aa6e28",  # Brown
        "#fffac8",  # Light Yellow
        "#800000",  # Maroon
        "#aaffc3",  # Mint
    ]

    def __init__(self, frame_width: int = 600, frame_height: int = 400):
        self.width = frame_width
        self.height = frame_height

    def typwritter(self, text: str, writer, interval: float):
        s = ""
        for char in text:
            writer(s + "**" + char + "**")
            s += char
            time.sleep(interval)

        writer(text)

    def code(
        self,
        text: str,
        language,
        line_numbers: bool = False,
        wrap: bool = False,
        interval: float = 0.05,
    ):
        div = st.empty()

        s = ""
        for char in text:
            s += char
            div.code(s, language=language, line_numbers=line_numbers, wrap_lines=wrap)
            time.sleep(interval)
        return div

    def write(self, text: str, interval: float = 0.05):
        """
        Write text to the streamlit app with a typing effect.
        """
        text = text.replace("\n", "  \n")
        div = st.empty()

        self.typwritter(text, div.write, interval)

    def latex(self, text: str, interval: float = 0.05):
        """
        Write LaTeX text to the streamlit app.
        """
        div = st.empty()
        self.typwritter(text, div.latex, interval)

    def draw_angle(
        self,
        points: list[Point],
        polygon: bool = False,
        show_side_diff: bool = False,
        allowed_diff: int = None,
        height: int = None,
        width: int = None,
        stroke_width: int = 3,
        stroke_color: str = "black",
        duration: float = 0.5,
    ):
        """
        - Draw an angle between three points.
        - need to provide `allowed_diff` if `show_side_diff` is True
        """
        if height is None:
            height = self.height
        if width is None:
            width = self.width

        colors = [stroke_color] * len(points)
        text_fill = "black"
        if show_side_diff:
            colors = self.__choose_side_colors(points=points, allowed_diff=allowed_diff)

        div = st.empty()
        img = Image.new("RGB", (width, height), (255, 255, 255))
        draw = ImageDraw.Draw(img)

        for idx in range(len(points) - 1):
            a, b = points[idx], points[idx + 1]
            draw.line((a.x, a.y, b.x, b.y), fill=colors[idx], width=stroke_width)
            angle_name = chr(ord("A") + idx)
            draw.text((a.x + 5, a.y - 5), text=angle_name, fill=text_fill)

        last = points[-1]
        angle_name = chr(ord("a") + len(points) - 1)
        draw.text((last.x + 5, last.y - 5), text=angle_name, fill=text_fill)
        if polygon:
            first = points[0]
            draw.line(
                (last.x, last.y, first.x, first.y),
                fill=colors[-1],
                width=stroke_width,
            )

        div.image(img)

    def draw_lines(
        self,
        startpoints=list[Point],
        endpoints=list[Point],
        height: int = None,
        width: int = None,
        stroke_width: int = 3,
        stroke_color: str = "black",
        duration: float = 0.5,
    ):
        """
        Draw lines between points.
        """
        if len(startpoints) != len(endpoints):
            raise ValueError(
                f"startpoints and endpoints must have the same length {len(startpoints)} != {len(endpoints)}"
            )
        if height is None:
            height = self.height
        if width is None:
            width = self.width
        div = st.empty()
        img = Image.new("RGB", (width, height), (255, 255, 255))
        draw = ImageDraw.Draw(img)
        for p1, p2 in zip(startpoints, endpoints):
            draw.line(
                (p1.x, p1.y, p2.x, p2.y),
                fill=stroke_color,
                width=stroke_width,
            )
        div.image(img)

    def __choose_side_colors(
        self,
        points: list[Point],
        allowed_diff: int,
    ) -> list:
        n = len(points)
        sides = [points[(i + 1) % n].distance_from(points[i]) for i in range(n)]

        def allowed(a, b):
            return abs(a - b) < allowed_diff

        groups = []
        for idx, length in enumerate(sides):
            placed = False

            for group in groups:
                if allowed(group[0][1], length):
                    group.append((idx, length))
                    placed = True
                    break

            if not placed:
                groups.append([(idx, length)])

        side_colors = [None] * len(sides)

        for idx, group in enumerate(groups):
            color = self.BASE_COLORS[idx % len(self.BASE_COLORS)]
            for idx, _ in group:
                side_colors[idx] = color

        return side_colors
