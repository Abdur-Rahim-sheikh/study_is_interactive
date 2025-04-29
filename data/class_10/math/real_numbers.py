import streamlit as st

from domain import BasePage
from domain.services import GraphVisualize
from public.resources.class_10.math.real_numbers import RealNumbers as numberCategorize
from domain.utils.to_bangla_digit import toBanglaDigit

class RealNumbers(BasePage):
    def __init__(self):
        super().__init__(file_location=__file__)

    def build_page(self, **args):
        pass

    def take_input(self):
        col1, col2, col3 = st.columns(3)
        with col1:
            chosen_option = st.radio(
                label= " ইনপুটের ধরন নির্বাচন করুন",
                options=["দশমিক", "ভগ্নাংশ", "মিশ্র"],
                index=0,
            )
        with col2:
            apostrophe = False
            whole_number = 0
            render = ""
            number = None
            if chosen_option == "দশমিক": 
                value = st.text_input(
                    label =  "একটি বাস্তব সংখ্যা লিখুনঃ ",
                    placeholder = "1.25'243'",
                    value="0",  
                    help = "- আপনি এপস্ট্রপি লিখতে চাইলে (') ব্যবহার করুন। - যেমনঃ 520.235'0238'",
                )
                
                if "'" in value:
                    apostrophe = True
                number = float(value.replace("'", ""))
                render = toBanglaDigit(value.replace("'", r"^\circ"))
            else:
                render = ""
                with st.container(height=100):
                    col21, col22, col23 = st.columns(3)
                    with col21:
                        if chosen_option == "মিশ্র":
                            whole_number = st.number_input(
                                label = "পূর্ণ সংখ্যা",
                                help = "একটি পূর্ণ সংখ্যা লিখুন",
                                min_value = 1,
                                format = "%d",
                            )
                            render = fr"{toBanglaDigit(whole_number)}\ "
                    
                    with col22:
                        numerator = st.number_input(
                            label = "লবঃ",
                            format = "%d",
                            step = 1,
                            value = 1,
                            help = "একটি পূর্ণ সংখ্যা লিখুন",
                        )
                    with col23:
                        denominator = st.number_input(
                            label = "হরঃ",
                            min_value = 1,
                            format = "%d",
                            help = "একটি পূর্ণ সংখ্যা লিখুন",
                        )

                number = (whole_number * denominator + numerator)/ denominator
                render += fr"\frac{{{toBanglaDigit(numerator)}}}{{{toBanglaDigit(denominator)}}}"
            
        with col3:
            st.latex(fr"\textcolor{{green}}{{আপনার\ সংখ্যাঃ \quad {render}}}")

        return number, chosen_option, apostrophe, whole_number



realNumbers = RealNumbers()
categorizer = numberCategorize()
categories = categorizer.getCategories
finalCategories = categorizer.getFinalCategories
graph = categorizer.getGraph


animator = GraphVisualize(graph=graph)

number, number_format, apostrophe, whole_number = realNumbers.take_input()

selected = st.pills(
    label="এটা কোন ধরনের বাস্তব সংখ্যা?",
    options=finalCategories,
    selection_mode="single",
)


if selected and st.button("চেক করুন"):
    paths = categorizer.categorize(number, apostrophe=apostrophe, number_format=number_format)
    answers = set(path[-1] for path in paths)
    st.write(number, paths)
    if selected in answers:
        st.write(f"হুররাহ! আপনার নির্বাচিত `{selected}` ক্যাটেগরিটি সঠিক!")
        st.balloons()
    else:
        st.write(f"দুঃখিত! আপনার নির্বাচিত `{selected}` ক্যাটেগরিটি সঠিক নয়।")

    
    for path in paths:
        # st.write(f"পথ: {path}")
        path = [(x, categories[x]) for x in path]
        animator.animate(path=path)
