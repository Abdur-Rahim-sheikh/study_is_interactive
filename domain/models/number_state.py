from dataclasses import dataclass


@dataclass
class NumberState:
    """
    All the variable keeps in decimal format, we format later using formatter
    """

    from_base: int
    to_base: int
    decimal_result: float
    decimal_partial: float = None

    def get_converter(self):
        """
        Get converter
        """
        convert = None
        if self.to_base == "binary":

            def convert(x):
                return bin(x)[2:]
        elif self.to_base == "octal":

            def convert(x):
                return oct(x)[2:]
        elif self.to_base == "decimal":

            def convert(x):
                return str(x)
        else:

            def convert(x):
                return hex(x)[2:]

        return convert

    def get_formated(self) -> dict:
        """
        Get formatted dict
        """
        convert = self.get_converter()

        return {
            "from_base": self.from_base,
            "to_base": self.to_base,
            "result": convert(self.decimal_result),
            "partial": convert(self.decimal_result) if self.decimal_partial else None,
        }
