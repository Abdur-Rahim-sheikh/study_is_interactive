def toRoman(num):
    mp = {
        1000: "M",
        900: "CM",
        500: "D",
        400: "CD",
        100: "C",
        90: "XC",
        50: "L",
        40: "XL",
        10: "X",
        9: "IX",
        5: "V",
        4: "IV",
        1: "I",
    }
    ans = ""
    for val, roman in mp.items():
        cnt = num // val
        ans += roman * cnt
        num -= val * cnt
    return ans
