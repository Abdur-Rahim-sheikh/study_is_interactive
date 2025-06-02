from dataclasses import dataclass


@dataclass
class NumberState:
    """
    All the variable keeps in decimal format, we format later using formatter
    """

    from_base: int
    to_base: int
    decimal_result: float
    decimal_partial: float = 0.0

    def __post_init__(self, precision: int = 8):
        self.precision = precision
        self.decimal_partial = round(self.decimal_partial, precision)
        self.decimal_result = round(self.decimal_result, precision)

    def from_decimal(self, number: float, base: int) -> str:
        int_part = int(number)
        decimal_part = float(number) - int_part
        char_box = "0123456789ABCDEF"
        answer_int = ""
        while int_part > 0:
            remainder = int_part % base
            int_part = int_part // base
            answer_int += char_box[remainder]

        answer_int = answer_int[::-1]
        answer_frac = ""
        precision = self.precision
        while decimal_part > 0 and precision > 0:
            decimal_part *= base
            int_part = int(decimal_part)
            decimal_part -= int_part
            answer_frac += char_box[int_part]
            precision -= 1
        answer = answer_int
        if answer_frac:
            answer += "." + answer_frac
        if not answer:
            answer = "0"
        return answer

    @property
    def formated(self) -> dict:
        """
        Get formatted dict
        """
        return {
            "from_base": self.from_base,
            "to_base": self.to_base,
            "result": self.from_decimal(self.decimal_result, self.to_base),
            "partial": self.from_decimal(self.decimal_partial, self.to_base),
        }
