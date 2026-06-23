def calculate_summary(transactions: list, metadata: dict) -> dict:
    debits = [t for t in transactions if t["type"] == "debit"]
    credits = [t for t in transactions if t["type"] == "credit"]

    total_debits = round(sum(t["amount"] for t in debits), 2)
    total_credits = round(sum(t["amount"] for t in credits), 2)

    # spending by category
    categories = {}
    for t in debits:
        cat = t["category"]
        categories[cat] = round(categories.get(cat, 0) + t["amount"], 2)

    # sort categories by spend
    categories = dict(sorted(categories.items(), key=lambda x: x[1], reverse=True))

    return {
        "total_debits": total_debits,
        "total_credits": total_credits,
        "net_cashflow": round(total_credits - total_debits, 2),
        "transaction_count": len(transactions),
        "debit_count": len(debits),
        "credit_count": len(credits),
        "spending_by_category": categories,
        "top_expense": max(debits, key=lambda x: x["amount"]) if debits else None
    }