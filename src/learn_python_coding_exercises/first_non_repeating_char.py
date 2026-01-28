"""
     🔹 Problem 6 — Pattern / Thinking Question (Hard)

Question
Find the first non-repeating character in a string.

Input

"automation"


Output

"u"


If none exists, return None.
"""

from collections import Counter
from typing import Any


def first_non_repeating_char(s: str) -> Any:
    temp = Counter(s)
    for x in temp.keys():
        if temp[x] == 1:
            return x
    return None

if __name__ == "__main__":
    print(first_non_repeating_char("abcaaabb"))
