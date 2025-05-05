import time

import streamlit as st


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
