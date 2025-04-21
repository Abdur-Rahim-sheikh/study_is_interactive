import streamlit as st
from domain import Base
import os
def main():
    st.header("Hello, there!")
    classes = os.listdir("data")
    pg = st.navigation(
        [
            st.Page()
        ]
    )
if __name__ == "__main__":
    main()
