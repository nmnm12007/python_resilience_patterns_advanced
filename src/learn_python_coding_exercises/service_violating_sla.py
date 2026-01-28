"""
🔹 Problem 7 — Real Automation-Style Problem (Hard)

Question
Given API response times, identify services that violate SLA.

Input

response_times = {
    "auth": [120, 110, 90],
    "payment": [300, 350, 400],
    "inventory": [200, 180]
}

SLA = 250


Output

["payment"]


Rule:

SLA violation = average response time > SLA


"""

def service_above_sla(resp:dict, sla:int) -> list:
    out_dict = {}
    for key in resp:
        value = resp[key]
        avg_value = sum(value) / len(value)
        if avg_value >= sla:
            out_dict.update({key: avg_value})

    print(out_dict)
    tmp_list = [x for x in out_dict]
    print(tmp_list)
    return tmp_list

if __name__ == "__main__":
    response_times = {
        "auth":[120, 110, 90],
        "payment":[300, 350, 400],
        "inventory":[200, 380]
    }
    service_above_sla(response_times, sla=250)