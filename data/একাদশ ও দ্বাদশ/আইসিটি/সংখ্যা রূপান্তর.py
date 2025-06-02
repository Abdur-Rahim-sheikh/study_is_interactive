import streamlit as st

from domain import BasePage
from domain.services import Animate, NumberConverter


class NumberConversion(BasePage):
    def __init__(self):
        super().__init__(__file__, page_icon=":material/sync_alt:")
        self.nc = NumberConverter()
        self.animate = Animate()
        self.available_bases = self.nc.available_bases

    def form(self) -> tuple:
        with st.form("number_conversion"):
            col1, col2, col3 = st.columns(
                [3, 1, 1], vertical_alignment="bottom", gap="large"
            )
            num = col1.text_input("যেই নাম্বারটিকে কনভার্ট করতে চান")

            base_from = col2.selectbox(
                label="হতে",
                options=self.available_bases,
                format_func=lambda x: self.available_bases[x],
                key="base1",
            )
            base_to = col3.selectbox(
                label="হবে",
                options=self.available_bases,
                format_func=lambda x: self.available_bases[x],
                key="base2",
            )

            submitted = st.form_submit_button("কনভার্ট করুন")
            if submitted:
                base = self.nc.get_base(base_from)
                if not self.nc.valid(num, base):
                    st.error(
                        f"{num} সংখ্যাটি {self.nc.available_bases[base_from]} বেস ফরম্যাটে নেই"
                    )
                else:
                    return num, base_from, base_to

    def via_decimal(self, description):
        col1, col2, col3 = st.columns(3)
        with col1:
            self.animate.write(description["to_decimal"])
        with col2:
            self.animate.code(
                description["from_decimal"]["integer_part"],
                language=None,
                line_numbers=True,
                wrap=True,
            )
        with col3:
            self.animate.code(
                description["from_decimal"]["fraction_part"],
                language="text",
                wrap=True,
            )

    def via_binary(self, description):
        col1, col2 = st.columns(2)
        with col1:
            self.animate.code(
                description["to_binary"], language=None, line_numbers=True
            )
        with col2:
            self.animate.code(
                description["from_binary"], language=None, line_numbers=True
            )

    def build_page(self):
        response = self.form()
        if not response:
            return
        num, base_from, base_to = response

        through_bin = "decimal" not in [base_to, base_from]
        if through_bin:
            tab1, tab2 = st.tabs(["দশমিক হয়ে", "বাইনারি হয়ে"])
        else:
            tab1 = st.tabs(["দশমিক হয়ে"])[0]
        with tab1:
            answer, description = self.nc.convert_via_decimal(num, base_from, base_to)
            self.via_decimal(description=description)
            st.write(
                f"অর্থাৎ {self.nc.available_bases[base_to]} এ রুপান্তরকৃত উত্তরটি হল {answer}"
            )
        if not through_bin:
            return
        with tab2:
            answer, description = self.nc.convert_via_binary(num, base_from, base_to)
            self.via_binary(description)

            st.write(
                f"অর্থাৎ {self.nc.available_bases[base_to]} এ রুপান্তরকৃত উত্তরটি হল {answer}"
            )


nc = NumberConversion()
nc.info(message="🚧 Under construction")
nc.build_page()
