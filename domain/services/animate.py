import time

import streamlit as st
from domain.models import Point
from PIL import ImageDraw, Image


class Animate:
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
        self, a: Point, b: Point, c: Point, angle: float = 0, interval: float = 0.05
    ):
        """
        Draw an angle between three points.
        """
        div = st.empty()
        img = Image.new("RGB", (500, 500), (255, 255, 255))
        draw = ImageDraw.Draw(img)
        draw.line((a.x, a.y, b.x, b.y), fill="black", width=2)
        draw.line((b.x, b.y, c.x, c.y), fill="black", width=2)
        draw.text((b.x + 10, b.y - 10), f"{angle:.2f}°", fill="black")
        div.image(img)
