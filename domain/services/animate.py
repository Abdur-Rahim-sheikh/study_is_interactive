import time

import streamlit as st


class Animate:
    def write(self, text: str, interval: float = 0.05):
        """
        Write text to the streamlit app with a typing effect.
        """
        div = st.empty()
        s = ""
        for char in text:
            div.markdown(s + "**" + char + "**")
            s += char
            time.sleep(interval)
        div.markdown(s)
