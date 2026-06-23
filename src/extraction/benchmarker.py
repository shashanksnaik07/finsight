class FinancialBenchmarker:
    def __init__(self):
        # 50/30/20 rule thresholds
        self.needs_threshold = 0.50      # rent, utilities, groceries
        self.wants_threshold = 0.30      # entertainment, dining, shopping
        self.savings_threshold = 0.20    # net savings rate

        self.needs_categories = {"rent", "utilities", "food", "health"}
        self.wants_categories = {"entertainment", "shopping", "transport", 
                                  "subscription", "other"}

    def benchmark(self, calculated_summary: dict) -> dict:
        total_debits = calculated_summary["total_debits"]
        total_credits = calculated_summary["total_credits"]
        spending = calculated_summary["spending_by_category"]

        # Calculate needs vs wants
        needs_total = sum(
            amount for cat, amount in spending.items()
            if cat in self.needs_categories
        )
        wants_total = sum(
            amount for cat, amount in spending.items()
            if cat in self.wants_categories
        )

        needs_pct = round((needs_total / total_credits) * 100, 1) if total_credits else 0
        wants_pct = round((wants_total / total_credits) * 100, 1) if total_credits else 0
        savings_pct = round(((total_credits - total_debits) / total_credits) * 100, 1) if total_credits else 0

        # Generate flags
        flags = []
        recommendations = []

        if needs_pct > 50:
            flags.append("HIGH_NEEDS")
            recommendations.append(
                f"Your essential expenses are {needs_pct}% of income — above the 50% guideline. "
                f"Rent is likely the main driver. Consider if housing costs can be reduced."
            )

        if wants_pct > 30:
            flags.append("HIGH_WANTS")
            recommendations.append(
                f"Your discretionary spending is {wants_pct}% of income — above the 30% guideline. "
                f"Review shopping and entertainment expenses."
            )

        if savings_pct < 20:
            flags.append("LOW_SAVINGS")
            recommendations.append(
                f"You are saving {savings_pct}% of income — below the 20% guideline. "
                f"Target saving at least ${round(total_credits * 0.20, 2)} per month."
            )
        else:
            flags.append("HEALTHY_SAVINGS")
            recommendations.append(
                f"Your savings rate is {savings_pct}% — above the 20% guideline. Good discipline."
            )

        return {
            "income": total_credits,
            "total_expenses": total_debits,
            "needs_total": round(needs_total, 2),
            "wants_total": round(wants_total, 2),
            "savings_total": round(total_credits - total_debits, 2),
            "needs_pct": needs_pct,
            "wants_pct": wants_pct,
            "savings_pct": savings_pct,
            "flags": flags,
            "recommendations": recommendations,
            "rule": "50/30/20"
        }