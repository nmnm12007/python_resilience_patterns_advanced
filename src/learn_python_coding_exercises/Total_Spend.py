"""
🔹 Problem 4 — Business Logic (Medium)

Question
Given transaction records, calculate total spend per user.

Input

transactions = [
    ("user1", 100),
    ("user2", 200),
    ("user1", 50),
    ("user3", 300),
    ("user2", 100)
]


Output

{
    "user1": 150,
    "user2": 300,
    "user3": 300
}

"""


def business_logic(transactions: list) -> dict:
    out_dict = {}
    for tmp_tuple in transactions:
        print(tmp_tuple)
        x,y = tmp_tuple
        print(x, ":", y)
        if x not in out_dict:
            out_dict[x] = y
        else:
            out_dict[x] += y
    print(out_dict)
    return  out_dict


if __name__ == "__main__":
    transactions = [
        ("user1", 100),
        ("user2", 200),
        ("user1", 50),
        ("user3", 300),
        ("user2", 100)
    ]

    business_logic(transactions)
