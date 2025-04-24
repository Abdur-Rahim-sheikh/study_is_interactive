import streamlit as st
from pathlib import Path
from domain import Base
import os

if "grade" not in st.session_state:
    st.session_state["grade"] = None

st.write(st.session_state)
GRADE_SRC = "data"
grades = [None] + [grade for grade in os.listdir(GRADE_SRC) ]

def homeView():
    st.header(f"হোম পেজ!")
    grade = st.selectbox("কোন ক্লাস দেখতে চান?", grades, key="selected_grade")

    if st.button("ক্লাস দেখুন"):
        st.session_state.grade = st.session_state.selected_grade
        st.rerun()

def backToHome():
    # st.session_state.grade = None
    st.info("Back to home")
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

if st.session_state.grade:
    path = os.path.join(GRADE_SRC, st.session_state.grade)
    books = getBooks(path)
    pg = st.navigation({"হোম": [st.Page(backToHome, title="হোম ফিরে যাই")]} | books)
else:
    pg = st.navigation([st.Page(homeView)])

pg.run()