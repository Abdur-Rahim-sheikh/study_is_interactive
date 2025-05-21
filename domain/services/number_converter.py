class NumberConverter:
    NUMBER_TYPES = {
        "বাইনারি": "binary",
        "অক্ট্যাল": "octal",
        "দশমিক": "decimal",
        "হেক্সাডেসিমেল": "hexadecimal",
    }

    @staticmethod
    def get_available_names(self) -> dict:
        return self.NUMBER_TYPES

    def get_permitted_digits(self, base: int) -> set:
        # fmt: off
        allowed = [".","0", "1","2", "3", "4", "5", "6","7", "8", 
                   "9","A", "B", "C", "D", "E", "F"],
        # fmt: onn
        return set(allowed[:base+1])

    def valid(self, number: str, base: int):
        allowed = self.get_permitted_digits(base)
        return all(ch in allowed for ch in str)

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

    def convert(self, number: str, convert_from: str, convert_to: str) -> str:
        base1, base2 = self.get_base(convert_from), self.get_base(convert_to)

        if not self.valid(number, base1):
            raise ValueError(f"{number} টি {convert_from} বেস ফরম্যাটে নেই")
