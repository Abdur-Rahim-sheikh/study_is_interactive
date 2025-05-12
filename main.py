from pathlib import Path, PosixPath

import streamlit as st

if "grade" not in st.session_state:
    st.session_state["grade"] = None

GRADE_SRC = "data"
grades = [None] + [grade.name for grade in Path(GRADE_SRC).iterdir()]


def homeView():
    st.set_page_config(page_title="হোম পেজ", layout="centered")
    st.header("হোম পেজ!")
    grade = st.selectbox("কোন ক্লাস দেখতে চান?", grades, key="selected_grade")

    if grade and st.button("ক্লাস দেখুন"):
        st.session_state.grade = grade
        st.rerun()


def backToHome():
    st.session_state.grade = None
    st.rerun()


def getTopics(chapter_path: PosixPath):
    topics = []

    for topic in chapter_path.iterdir():
        if not topic.suffix == ".py" or topic.stem.startswith("__"):
            continue

        topics.append(st.Page(str(topic.absolute()), title=topic.stem))
    return topics


def getBooks(grade_path: Path):
    books = {}
    for chapter in Path(grade_path).iterdir():
        books[chapter.name] = getTopics(chapter)
    return books


grade = st.session_state.grade

if grade:
    path = Path(GRADE_SRC, grade)
    books = getBooks(path)
    # settings =
    pg = st.navigation(books | {"আরো": [st.Page(backToHome, title="হোমে ফিরে যাই")]})
else:
    pg = st.navigation([st.Page(homeView)])

pg.run()
