"""
🔹 Problem 2 — Dictionary + Loop (Easy–Medium)

Question
Given a list of integers, return a dictionary with frequency of each number.

Input

[1, 2, 2, 3, 1, 4, 2]


Output

{1: 2, 2: 3, 3: 1, 4: 1}

"""

from collections import Counter

def frequency_numbers(nums:list) -> dict:

    temp = Counter(nums)
    print(temp)
    count_dict = {x:y for x, y in temp.items()}
    print(count_dict)
    return count_dict

if __name__ == '__main__':
    frequency_numbers([1, 2, 2, 3, 1, 4, 2])

# Alternative Logic

    # 
    # for x in lst:
    #     if x not in out_dict:
    #         out_dict.update({x: this_cnt})
    #     else:
    #         this_cnt += 1
    #         out_dict.update({x: this_cnt})
    # print(out_dict)