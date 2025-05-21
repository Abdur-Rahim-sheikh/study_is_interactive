from dataclasses import dataclass


@dataclass
class NumberState:
    first_operand: int
    second_operand: int
    result: int
    after_decimal: bool = False
