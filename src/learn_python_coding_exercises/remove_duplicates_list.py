"""
🔹 Problem 3 — List Transformation (Medium)

Question
Write a function remove_duplicates_preserve_order(lst: list) -> list

Input

[3, 1, 2, 3, 2, 4, 1]


Output

[3, 1, 2, 4]


⚠️ Order matters.
"""

def remove_duplicates_preserve_order(lst: list) -> list:
    """

    :param lst: 
    """

    out_list = []
    for x in lst:
        if x not in out_list:
            out_list.append(x)
    print(out_list)
    return out_list


if __name__ == "__main__":
    lst = [1, 2, 3, 2, 4, 1]
    remove_duplicates_preserve_order(lst)

    


        
