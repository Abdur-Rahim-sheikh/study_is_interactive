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
        else:
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
        return state

    def convert_from_decimal(self, number: str, base: int) -> list[NumberState]:
        int_part = int(number)
        decimal_part = float(number) - int_part
        states = []

        while int_part > 0:
            remainder = int_part % base
            int_part = int_part // base
            states.append(
                NumberState(
                    from_base=10,
                    to_base=base,
                    decimal_result=int_part,
                    decimal_partial=remainder,
                )
            )

        mx = 10
        while decimal_part > 0 and mx > 0:
            decimal_part *= base
            int_part = int(decimal_part)
            decimal_part -= int_part
            states.append(
                NumberState(
                    from_base=10,
                    to_base=base,
                    decimal_result=decimal_part,
                    decimal_partial=int_part,
                )
            )
            mx -= 1
        return states

    def convert(
        self, number: str, convert_from: str, convert_to: str
    ) -> list[NumberState]:
        base1, base2 = self.get_base(convert_from), self.get_base(convert_to)

        if not self.valid(number, base1):
            raise ValueError(f"{number} টি {convert_from} বেস ফরম্যাটে নেই")

        states = []
        if base1 != 10:
            state = self.convert_to_decimal(number, base1)
            number = state.decimal_result
            states.append(state)

        if base2 != 10:
            next_states = self.convert_from_decimal(number, base2)
            states.extend(next_states)

        return states
