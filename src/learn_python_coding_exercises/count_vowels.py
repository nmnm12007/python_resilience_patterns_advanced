
"""
    🔹 Problem 1 — String Processing (Easy)

Question
Write a function count_vowels(s: str) -> dict that returns the count of each vowel (a, e, i, o, u) in the string.

Input

"automation"


Output

{'a': 2, 'e': 0, 'i': 0, 'o': 2, 'u': 1}


Constraints:

Case insensitive

Include vowels with zero count

"""


from collections import Counter

def count_vowels(text: str) -> dict:
    out_dict = {}
    vowel_list = ["a", "e", "i", "o", "u"]
    count_dict = Counter(text)
    for x in list(text.lower()):
        out_dict[x] = count_dict.get(x, 0)
        
    return count_dict


    




if __name__ == "__main__":
    # count_vowels("Hello World")
    count_vowels("automation")
    