"""
🔹 Problem 5 — Error Handling + Logic (Medium–Hard)

Question
Write a function safe_divide(numbers: list, divisor: int) -> list

Rules:

Divide each number by divisor

If divisor is 0, return empty list

Ignore non-numeric values

Input

numbers = [10, 20, "x", 30]
divisor = 10


Output

[1.0, 2.0, 3.0]

"""

def safe_divide(numbers: list, divisor: int) -> list:
    out_list = []

    if divisor == 0 or type(divisor) != int:
        return []
    else:
        for number in numbers:
            if type(number) == int: 
                out_list.append(number / divisor)
        print(out_list)
    return out_list
# REFER THIS
# def safe_divide(numbers, divisor):
#     if not isinstance(divisor, int) or divisor == 0:
#         return []
#     return [n / divisor for n in numbers if isinstance(n, (int, float))]

if __name__ == "__main__":
    numbers_1 = [10, 20, "x", 30]
    divisor_2 = 10
    safe_divide(numbers_1, divisor_2)



