"""
   Write a function analyze_latency(data: dict) -> dict that returns:

Average response time per service (rounded to 2 decimals)

Name of the slowest service (highest average)

Expected Output
{
    "averages": {
        "auth": 117.0,
        "payment": 296.67,
        "inventory": 195.0
    },
    "slowest_service": "payment"
}

🧠 What I’m Evaluating (Mentor Lens)

For each problem, I’m checking:

Logical correctness

Use of core Python (dict, loops, functions)

Edge-case awareness

Readability (very important)

I do not care about:

One-liners

Fancy tricks

Over-engineering
"""

def analyze_latency(resp_time: dict) -> dict:
    out_dict = {}
    max_avg = 0.0
    slowest_service = None

    for x,y in resp_time.items():
        avg = round(sum(y) / len(y),2)
        out_dict[x] = avg

        if avg > max_avg:
            max_avg = avg
            slowest_service = x

    return {"averages": out_dict,
            "slowest_service": slowest_service
            }