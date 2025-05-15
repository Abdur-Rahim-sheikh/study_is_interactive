from pathlib import Path, PosixPath

import streamlit as st

if "grade" not in st.session_state:
    st.session_state["grade"] = None

GRADE_SRC = "data"
grades = [None] + [grade.name for grade in Path(GRADE_SRC).iterdir()]


def homeView():
    st.set_page_config(page_title="হোম পেজ", layout="centered")
    st.header("Interactive Study")
    st.subheader("ইন্টারেক্টিভ স্টাডি প্ল্যাটফর্ম")

    grade = st.selectbox("কোন ক্লাস দেখতে চান?", grades, key="selected_grade")

    if grade and st.button("প্রবেশ করুন"):
        st.session_state.grade = grade
        st.rerun()

    with st.expander(
        "এপটি আপনাকে যেভাবে সাহায্য করবে ", expanded=True, icon=":material/page_info:"
    ):
        story = """
        বাংলাদেশের এনসিটিবি (nctb) প্রণোদিত বইয়ের উপর তৈরি করা হয়েছে এই এপটিকে। 
        প্রতিটা বইয়ে এমন কিছু টপিক থাকে, যা বার বার প্রাকটিস করলে ভালো হয়।
        সেটা হওয়া দরকার আমাদের খেয়াল খুশি মত, আমার আরামের সময় মত। কিন্তু সবসময় তো আমাদের সামনে শিক্ষক থাকা সম্বভ না। 
        তাহলে আমার প্রাকটিস করা বিষয়টী সঠিক নাকি ভুল কিভাবে বুঝবো? এমন সময় কাজে আসবে এই এপটি।
        প্রথমে ড্রপডাউন থেকে ক্লাস সিলেক্ট করুন। এরপর ক্লাসের বই ও টপিকগুলো বাম পাশের সাইড বারে দেখতে পাবেন। 
        সেখান থেকে আপনার পছন্দের টপিক সিলেক্ট করুন।
        ওই টপিকের পেজে যদি বুঝতে না পারেন যে কি করতে হবে, তাহলে টপিকের নামের নিচে থাকা ইনফো বাটনে ক্লিক করুন।"""
        st.write(story)
        st.write(
            "যেকোনো এনসিটিবি বই অনলাইনে অফিসিয়াল পেজ থেকে পিডিএফ ডাউনলোড করতে নিচের লিংকে যান"
        )
        st.markdown(
            "[এনসিটিবি বইয়ের ২০২৫](https://nctb.portal.gov.bd/site/page/d01e72b0-8ecd-4c81-bffd-c9e117b7fdad/-)"
        )
    st.warning("এপটি মোবাইলে ব্যবহারের জন্য তৈরি করা হয় নি, ল্যাপটপ বা ডেস্কটপে ব্যবহার করুন।")


def backToHome():
    st.session_state.grade = None
    st.rerun()


def getTopics(chapter_path: PosixPath):
    topics = []
    names = list(chapter_path.iterdir())

    for topic in sorted(names):
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
