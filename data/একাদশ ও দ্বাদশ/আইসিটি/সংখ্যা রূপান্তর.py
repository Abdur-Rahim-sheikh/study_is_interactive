import streamlit as st

from domain import BasePage
from domain.models import NumberState
from domain.services import Animate, NumberConverter


class NumberConversion(BasePage):
    def __init__(self):
        super().__init__(__file__, page_icon=":material/sync_alt:")
        self.nc = NumberConverter()
        self.animate = Animate()
        self.available_bases = self.nc.get_available_bases()

    def __prepare_decimal_integer(self, states: list[NumberState], number: str):
        lines = []
        first = f"{states[0].to_base} | {number}   LSB"
        lines.append(first)
        for state in states[:-1]:
            intermediate = (
                f"{state.to_base} | {state.decimal_result} -> {state.decimal_partial}"
            )
            lines.append(intermediate)

        last = f"{states[-1].to_base} | {states[-1].decimal_result}   MSB"
        lines.append(last)
        return "\n".join(lines)

    def form(self) -> tuple:
        with st.form("number_conversion"):
            num = st.text_input("যেই নাম্বারটিকে কনভার্ট করতে চান")
            base_from = st.selectbox(
                label="",
                options=self.available_bases,
                format_func=lambda x: self.available_bases[x],
                label_visibility="collapsed",
                key="base1",
            )
            base_to = st.selectbox(
                label="",
                options=self.available_bases,
                format_func=lambda x: self.available_bases[x],
                label_visibility="collapsed",
                key="base2",
            )
            submitted = st.form_submit_button("কনভার্ট করুন")
            if submitted:
                base = self.nc.get_base(base_from)
                if not self.nc.valid(num, base):
                    st.error(f"{num} টি {base_from} বেস ফরম্যাটে নেই")
                else:
                    return num, base_from, base_to

    def build_page(self):
        response = self.form()
        if not response:
            return
        num, base_from, base_to = response
        states = self.nc.convert(num, base_from, base_to)
        decimal_part = self.__prepare_decimal_integer(states, num)
        self.animate.code(decimal_part, language=None)
        st.write(states)


nc = NumberConversion()
nc.build_page()
nc.info(message="🚧 Under construction")
