import time

import streamlit as st
from PIL import Image, ImageDraw

from domain.models import Point


class Animate:
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

    def code(self, text: str, language, interval: float = 0.05):
        div = st.empty()

        s = ""
        for char in text:
            s += char
            div.code(s, language=language)
            time.sleep(interval)
        return div

    def write(self, text: str, interval: float = 0.05):
        """
        Write text to the streamlit app with a typing effect.
        """
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
        a: Point,
        b: Point,
        c: Point,
        angle: float = 0,
        height: int = None,
        width: int = None,
        stroke_width: int = 3,
        stroke_color: str = "black",
        duration: float = 0.5,
    ):
        """
        Draw an angle between three points.
        """
        if height is None:
            height = self.height
        if width is None:
            width = self.width
        div = st.empty()
        img = Image.new("RGB", (width, height), (255, 255, 255))
        draw = ImageDraw.Draw(img)
        draw.line((a.x, a.y, b.x, b.y), fill=stroke_color, width=stroke_width)
        draw.line((b.x, b.y, c.x, c.y), fill=stroke_color, width=stroke_width)
        # bc = b.distance_from(c)
        # ab = a.distance_from(b)
        # radius = 0.1 * min(bc, ab)
        # start_angle = a.angle_to(b)
        # end_angle = c.angle_to(b)
        draw.arc([a.x, a.y, c.x, c.y], 0, angle, fill=stroke_color, width=stroke_width)
        draw.text(
            (b.x + 5, b.y - 5),
            "θ",
            fill="black",
            font=None,
        )
        draw.text(
            (a.x + 5, a.y - 5),
            "A",
            fill="black",
            font=None,
        )
        draw.text(
            (b.x + 5, b.y + 5),
            "B",
            fill="black",
            font=None,
        )

        draw.text(
            (c.x + 5, c.y + 5),
            "C",
            fill="black",
            font=None,
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
