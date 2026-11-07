# Task 01 | Nested Transaction Analyzer

# Output totals: Sara=700, Ali=500.

def analyze_transactions(transactions):
    seen_ids = []
    for t in transactions:
        if t["id"] in seen_ids:
            raise ValueError("Duplicate transaction ID: " + str(t["id"]))
        seen_ids.append(t["id"])

    totals = {}
    categories = {}
    for t in transactions:
        totals[t["customer"]] = 0
        categories[t["customer"]] = {}

    for t in transactions:
        if t["status"] == "success":
            name = t["customer"]
            cat = t["category"]
            totals[name] += t["amount"]
            if cat not in categories[name]:
                categories[name][cat] = 0
            categories[name][cat] += t["amount"]

    report = [
        {
            "customer": name,
            "total": totals[name],
            "top_category": max(categories[name], key=categories[name].get)
                            if categories[name] else None,
        }
        for name in totals
    ]

    report.sort(key=lambda row: (-row["total"], row["customer"]))

    for i, row in enumerate(report, start=1):
        row["rank"] = i

    return report

data = [
    {"id": 1, "customer": "Ali",  "category": "Food",   "amount": 500, "status": "success"},
    {"id": 2, "customer": "Ali",  "category": "Travel", "amount": 200, "status": "failed"},
    {"id": 3, "customer": "Sara", "category": "Food",   "amount": 700, "status": "success"},
]

for row in analyze_transactions(data):
    print(row)