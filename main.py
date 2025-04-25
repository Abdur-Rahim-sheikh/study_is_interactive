import streamlit as st
from pathlib import Path
import os

if "grade" not in st.session_state:
    st.session_state["grade"] = None

GRADE_SRC = "data"
grades = [None] + [grade for grade in os.listdir(GRADE_SRC) ]



def homeView():
    st.set_page_config(
        page_title = "হোম পেজ",
        layout="centered"
    )
    st.header(f"হোম পেজ!")
    grade = st.selectbox("কোন ক্লাস দেখতে চান?", grades, key="selected_grade")

    if st.button("ক্লাস দেখুন"):
        st.session_state.grade = grade
        st.rerun()

def backToHome():
    st.session_state.grade = None
    st.rerun()

# apply caching later
def getTopics(chapter_path: Path):
    topics = []
    for topic in os.listdir(chapter_path):
        topics.append(st.Page(os.path.join(chapter_path, topic), title=topic.rstrip(".py")))
    return topics

# apply caching later
def getBooks(grade_path: Path):
    books = {}
    for chapter in os.listdir(grade_path):
        books[chapter] = getTopics(os.path.join(grade_path, chapter))
    return books


grade = st.session_state.grade

if grade:
    path = os.path.join(GRADE_SRC, grade)
    books = getBooks(path)
    # settings = 
    pg = st.navigation(
         books | {"আরো": [st.Page(backToHome, title="হোমে ফিরে যাই")]},
    )
else:
    pg = st.navigation([st.Page(homeView)])

pg.run()