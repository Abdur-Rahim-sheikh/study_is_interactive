import streamlit as st

from domain import BasePage
from domain.services import GraphVisualize
from public.resources.class_10.math.real_numbers import RealNumbers as numberCategorize


class RealNumbers(BasePage):
    def __init__(self):
        super().__init__(file_location=__file__)

    def build_page(self, **args):
        pass


realNumbers = RealNumbers()
categorizer = numberCategorize()
categories = categorizer.getCategories
finalCategories = categorizer.getFinalCategories
graph = categorizer.getGraph


animator = GraphVisualize(graph=graph)

number = st.number_input("Enter a number")

selected = st.pills(
    label="এটা কোন ধরনের বাস্তব সংখ্যা?",
    options=finalCategories,
    selection_mode="single",
)


if selected:
    st.write(f"আপনি `{selected}` ক্যাটেগরি নির্বাচন করেছেন।")
    paths = categorizer.categorize(number)
    st.write(paths)
    answers = set(path[-1] for path in paths)
    if selected in answers:
        st.write(f"আপনার সংখ্যা `{selected}` ক্যাটেগরির অন্তর্ভুক্ত।")
    else:
        st.write(f"আপনার সংখ্যা `{selected}` ক্যাটেগরির অন্তর্ভুক্ত নয়।")

    for path in paths:
        st.write(f"পথ: {path}")
        path = [(x, categories[x]) for x in path]
        animator.animate(path=path)
