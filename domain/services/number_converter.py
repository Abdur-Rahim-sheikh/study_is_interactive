from ..models import NumberState


class NumberConverter:
    NUMBER_TYPES = {
        "binary": "বাইনারি",
        "octal": "অক্ট্যাল",
        "decimal": "দশমিক",
        "hexadecimal": "হেক্সাডেসিমেল",
    }

    def get_available_bases(self) -> dict:
        return self.NUMBER_TYPES

    def get_permitted_digits(self, base: int) -> set:
        # fmt: off
        allowed = [".","0", "1","2", "3", "4", "5", "6","7", "8", 
                   "9","A", "B", "C", "D", "E", "F"]
        # fmt: on
        return set(allowed[: base + 1])

    def valid(self, number: str, base: int):
        allowed = self.get_permitted_digits(base)
        number = str(number)
        return all(ch in allowed for ch in number) and number.count(".") <= 1

    def get_base(self, type: str):
        base = None
        if type == "binary":
            base = 2
        elif type == "octal":
            base = 8
        elif type == "decimal":
            base = 10
        elif "hexadecimal":
            base = 16
        return base

    def convert_to_decimal(self, number: str, base: int) -> NumberState:
        idx = number.index(".") if "." in number else len(number)
        idx -= 1
        decimal = 0
        for ch in number:
            if ch == ".":
                continue
            decimal += int(ch, base) * (base**idx)
            idx -= 1
        state = NumberState(
            from_base=base,
            to_base=10,
            decimal_result=decimal,
        )
        return str(decimal), state

    def convert_from_decimal(self, number: str, base: int) -> list[NumberState]:
        int_part = int(number.split(".")[0])
        decimal_part = float(number) - int_part
        int_parts, frac_parts = [], []
        answer_int = ""
        while int_part > 0:
            remainder = int_part % base
            int_part = int_part // base
            tem = NumberState(
                from_base=10,
                to_base=base,
                decimal_result=int_part,
                decimal_partial=remainder,
            )
            answer_int += tem.formated["partial"]
            int_parts.append(tem)
        answer_int = answer_int[::-1]
        answer_frac = ""
        mx = 10
        while decimal_part > 0 and mx > 0:
            decimal_part *= base
            int_part = int(decimal_part)
            decimal_part -= int_part
            tem = NumberState(
                from_base=10,
                to_base=base,
                decimal_result=decimal_part,
                decimal_partial=int_part,
            )
            frac_parts.append(tem)
            answer_frac += tem.formated["partial"]
            mx -= 1
        answer = answer_int
        if answer_frac:
            answer += "." + answer_frac

        return answer, int_parts, frac_parts

    def describe_to_decimal(self, number: str, state: NumberState) -> str:
        base = state.from_base
        idx = number.index(".") if "." in number else len(number)
        idx -= 1
        tem = []
        for ch in number:
            if ch == ".":
                continue
            tem.append(f"{int(ch, base)} * {base}^{idx}")
            idx -= 1
        middle = " + ".join(tem)
        return f"{number}\n{middle}\n{state.decimal_result}"

    def describe_from_decimal(
        self, number: str, int_parts: list[NumberState], frac_parts: list[NumberState]
    ) -> str:
        if "." not in number:
            number += "."
        left, right = number.split(".")
        left, right = left.lstrip("0"), right.rstrip("0")
        lines = []

        if len(int_parts):
            tem = f"{int_parts[0].to_base} | {left}"
            lines.append(tem)
        last = int_parts.pop()
        for state in int_parts:
            tem = (
                f"{state.to_base} | {state.decimal_result} --> {state.decimal_partial}"
            )
            lines.append(tem)
        tem = f"{last.decimal_result} --> {last.decimal_partial}"
        lines.append(tem)
        answer_int = "\n".join(lines)

        lines = []
        if len(frac_parts):
            tem = f"{right}"
            lines.append(tem)
        for state in frac_parts:
            tem = f"{state.to_base}\n----------\n{state.decimal_partial} | {state.decimal_result:.5}"
            lines.append(tem)

        answer_frac = "\n".join(lines)
        return answer_int, answer_frac

    def convert(
        self, number: str, convert_from: str, convert_to: str
    ) -> list[NumberState]:
        """
        This returns the final `answer` and the `description` text in latex format
        The description is formatted as:
        {
            "to_decimal": str,
            "from_decimal":{
                "integer_part": str,
                "fraction_part": str
            }
        }
        """
        number = str(number)
        base1, base2 = self.get_base(convert_from), self.get_base(convert_to)

        if not self.valid(number, base1):
            raise ValueError(f"{number} টি {convert_from} বেস ফরম্যাটে নেই")

        to_decimal = []
        description = {
            "to_decimal": "",
            "from_decimal": {"integer_part": "", "fraction_part": ""},
        }
        answer = ""
        if base1 != 10:
            answer, state = self.convert_to_decimal(number, base1)
            description["to_decimal"] = self.describe_to_decimal(number, state)
            number = str(state.decimal_result)
            to_decimal.append(state)

        if base2 != 10:
            answer, int_parts, frac_parts = self.convert_from_decimal(number, base2)
            result_int, result_frac = self.describe_from_decimal(
                number, int_parts, frac_parts
            )
            description["from_decimal"] = {
                "integer_part": result_int,
                "fraction_part": result_frac,
            }

        return answer, description
