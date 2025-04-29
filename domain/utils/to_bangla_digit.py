def toBanglaDigit(number: str) -> str:
    """
    Convert English digits to Bangla digits.

    Args:
        number (str): The number to convert.

    Returns:
        str: The number with Bangla digits.
    """
    en_to_bn = str.maketrans("0123456789", "০১২৩৪৫৬৭৮৯")
    return str(number).translate(en_to_bn)