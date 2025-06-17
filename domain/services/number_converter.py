from ..models import NumberState
from math import log2


class NumberConverter:
    NUMBER_TYPES = {
        "binary": "বাইনারি",
        "octal": "অক্ট্যাল",
        "decimal": "দশমিক",
        "hexadecimal": "হেক্সাডেসিমেল",
    }

    @property
    def available_bases(self) -> dict:
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
            decimal_part = tem.decimal_result
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
            tem.append(f"{int(ch, base)} * {base}^{{{idx}}}")
            idx -= 1
        middle = " + ".join(tem)
        first = f"${number}_{{{base}}}$ সংখ্যাটিকে দশমিকে রূপান্তর করতে হবে"
        second = f"${middle}$"
        final = f"${state.decimal_result}_{{10}}$ -> হল আমাদের দশমিকে রূপান্তরকৃত মান"
        return f"{first}\n{second}\n{final}"

    def describe_from_decimal(
        self, number: str, int_parts: list[NumberState], frac_parts: list[NumberState]
    ) -> str:
        if "." not in number:
            number += "."
        left, right = number.split(".")
        left, right = left.lstrip("0"), "." + right.rstrip("0")
        lines = []
        padding = 0
        space = 2
        has_int = False
        tem = f"দশমিক পূর্ণসংখ্যা {left} এর রূপান্তর করি"
        lines.append(tem)
        if len(int_parts):
            tem = f"{int_parts[0].to_base} │ {left}"
            lines.append(tem)
            padding = len(tem) + 4
            has_int = True
        combined = ""
        for idx, state in enumerate(int_parts):
            lines.append(f"{' ' * space}╰{'─' * padding}")
            combined += str(state.formated["partial"])
            if idx + 1 == len(int_parts):
                tem2 = f"{' ' * (space + 2)}{state.decimal_result} ─── {state.decimal_partial}"
                if state.decimal_partial > 9:
                    tem2 += f"({state.formated['partial']})"
            else:
                tem2 = f"{state.to_base} │ {state.decimal_result} ─── {state.decimal_partial}"
                if state.decimal_partial > 9:
                    tem2 += f"({state.formated['partial']})"

            lines.append(tem2)
        tem = "এখানে ড্যাশ এর ডানপাশের ভাগশেষ গুলি নিচ থেকে উপরে সাজাই"
        lines.append(tem)
        tem = "সবচেয়ে নিচের অঙ্কটি সবচেয়ে গুরুত্বপূর্ণ (MSB) এবং সবচেয়ে উপরের অঙ্কটি সবচেয়ে কম গুরুত্বপূর্ণ (LSB)"
        lines.append(tem)
        lines.append("একত্র করে পাইঃ " + combined[::-1])

        answer_int = "\n".join(lines)

        lines = []
        space = 4

        padding = 5
        horizontal = 0
        has_frac = False
        tem = f"দশমিক ভগ্নাংশ {right} এর রূপান্তর করি"
        lines.append(tem)
        if len(frac_parts):
            space = len(right) + 2
            tem = f"{'#':<{padding - 1}}│{right:>{space}}"
            horizontal = len(tem) + 4
            lines.append(tem)
            has_frac = True
        combined = ""
        for state in frac_parts:
            combined += state.formated["partial"]
            tem1 = f"{'│':>{padding}}{'x ' + str(state.to_base):>{space}}"
            tem2 = "─" * horizontal
            decimal_result = str(round(state.decimal_result, 8)).strip("0")
            if decimal_result == ".":
                decimal_result = "0"
            tem3 = f"{state.decimal_partial:<{padding - 1}}│{decimal_result:>{space}}"
            lines.extend([tem1, tem2, tem3])

        tem = "এখানে ড্যাশ এর বামপাশের ভাগশেষ গুলি উপর থেকে নিচে সাজাই"
        lines.append(tem)
        tem = "সবচেয়ে উপরের অঙ্কটি সবচেয়ে গুরুত্বপূর্ণ (MSB) এবং সবচেয়ে নিচের অঙ্কটি সবচেয়ে কম গুরুত্বপূর্ণ (LSB)"
        lines.append(tem)
        lines.append("একত্র করে পাইঃ " + combined)
        answer_frac = "\n".join(lines)
        if not has_int:
            answer_int = ""
        if not has_frac:
            answer_frac = ""
        return answer_int, answer_frac

    def convert_via_decimal(
        self, number: str, convert_from: str, convert_to: str
    ) -> tuple[str, str]:
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
            raise ValueError(
                f"{number} টি {self.available_bases[convert_from]} বেস ফরম্যাটে নেই"
            )

        description = {
            "to_decimal": "",
            "from_decimal": {"integer_part": "", "fraction_part": ""},
        }
        answer = ""
        if base1 != 10:
            answer, state = self.convert_to_decimal(number, base1)
            description["to_decimal"] = self.describe_to_decimal(number, state)
            number = str(state.decimal_result)

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

    def __adjust_bin(self, bin, group):
        x = bin.split(".")
        if len(x) == 1:
            left, right = x[0], ""
        else:
            left, right = x
        if len(left) % group:
            rem = group - len(left) % group
            left = "0" * rem + left
        left = " ".join(left[i : i + group] for i in range(0, len(left), group))

        if len(right) % group:
            rem = group - len(right) % group
            right = right + "0" * rem
        right = " ".join(right[i : i + group] for i in range(0, len(right), group))

        ans = left
        if right:
            ans += " . " + right
        return ans

    def describe_binary(self, num: str, bin: str, group: int, to_bin=True) -> str:
        """Group can be in either 3 or 4"""
        adjusted_num = " ".join(f"{ch:^{group}}" if ch != "." else ch for ch in num)
        adjusted_bin = self.__adjust_bin(bin, group)
        ans = ""
        other = None
        if group == 4:
            other = self.available_bases["hexadecimal"]
        elif group == 3:
            other = self.available_bases["octal"]
        if to_bin:
            start = (
                f"{num} {other} সংখ্যাটির প্রতিটি অঙ্কের জন্য {group} অংক সমমান বাইনারি লিখি"
            )
            end = "তাহলে বাইনারিতে উত্তর পেলামঃ"
            ans = f"{start}\n{adjusted_num}\n{adjusted_bin}\n{bin}\n{end} {bin}"
        else:
            start = f"{bin} বাইনারি সংখ্যাটিকে প্রতি {group} অঙ্কের গ্রুপে বিভক্ত করি"
            end = f"আমাদের প্রাপ্ত {other} সংখ্যাঃ"
            ans = f"{start}\n{adjusted_bin}\n{adjusted_num}\n{num}\n{end} {num}"
        return ans

    def convert_via_binary(
        self, number: str, convert_from: str, convert_to: str
    ) -> tuple[str, str]:
        """
        This returns the final `answer` and the `description` text in latex format
        The description is formatted as:
        {
            "to_binary":str,
            "from_binary":str
        }
        This method accpets only 'binary','octal','hexadecimal'
        """
        number = str(number)
        base1, base2 = self.get_base(convert_from), self.get_base(convert_to)

        if not self.valid(number, base1):
            raise ValueError(
                f"{number} টি {self.available_bases[convert_from]} বেস ফরম্যাটে নেই"
            )
        if base1 == 10 or base2 == 10:
            raise ValueError(
                "এই শর্টকাটটি দশমিক এর জন্য সুবিধাজনক নয়।",
                "আপনি `বাইনারি`, `অক্ট্যাল` ও `হেক্সাডেসিম্যাল` এর সময় এই শর্টকাটটির সুন্দর্য উপভোগ করতে পারবেন",
            )

        description = {"to_binary": "", "from_binary": ""}
        decimal, _ = self.convert_to_decimal(number, base1)
        if base1 != 2:
            bin, _, _ = self.convert_from_decimal(decimal, 2)
            group = int(log2(base1))
            description["to_binary"] = self.describe_binary(
                num=number, bin=bin, group=group, to_bin=True
            )
            number = bin

        if base2 != 2:
            to_base2, _, _ = self.convert_from_decimal(decimal, base2)
            group = int(log2(base2))
            description["from_binary"] = self.describe_binary(
                num=to_base2, bin=number, group=group, to_bin=False
            )
            number = to_base2

        return number, description
