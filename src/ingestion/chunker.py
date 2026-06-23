import json
from pathlib import Path

class FinancialChunker:
    def chunk(self, processed_data: dict) -> list:
        chunks = []
        
        chunks += self._chunk_transactions(processed_data)
        chunks += self._chunk_category_summary(processed_data)
        chunks += self._chunk_overall_summary(processed_data)
        
        return chunks

    def _chunk_transactions(self, data: dict) -> list:
        chunks = []
        for t in data["transactions"]:
            text = (
                f"On {t['date']}, there was a {t['type']} of ${t['amount']} "
                f"for {t['description']} categorized as {t['category']}."
            )
            chunks.append({
                "text": text,
                "metadata": {
                    "type": "transaction",
                    "date": t["date"],
                    "amount": t["amount"],
                    "transaction_type": t["type"],
                    "category": t["category"],
                    "description": t["description"],
                    "file_name": data["file_name"]
                }
            })
        return chunks

    def _chunk_category_summary(self, data: dict) -> list:
        chunks = []
        spending = data["calculated_summary"]["spending_by_category"]
        total_debits = data["calculated_summary"]["total_debits"]

        for category, amount in spending.items():
            percentage = round((amount / total_debits) * 100, 1)
            text = (
                f"Total spending on {category} was ${amount}, "
                f"which is {percentage}% of total expenses for the period."
            )
            chunks.append({
                "text": text,
                "metadata": {
                    "type": "category_summary",
                    "category": category,
                    "amount": amount,
                    "percentage": percentage,
                    "file_name": data["file_name"]
                }
            })
        return chunks

    def _chunk_overall_summary(self, data: dict) -> list:
        calc = data["calculated_summary"]
        llm = data["llm_summary"]
        meta = data["metadata"]

        text = (
            f"Financial summary for {meta.get('account_holder', 'account holder')} "
            f"from {llm.get('period_start', 'unknown')} to {llm.get('period_end', 'unknown')}. "
            f"Opening balance: ${llm.get('opening_balance', 'N/A')}. "
            f"Closing balance: ${llm.get('closing_balance', 'N/A')}. "
            f"Total credits: ${calc['total_credits']}. "
            f"Total debits: ${calc['total_debits']}. "
            f"Net cashflow: ${calc['net_cashflow']}. "
            f"Top expense was {calc['top_expense']['description']} at ${calc['top_expense']['amount']}."
        )

        return [{
            "text": text,
            "metadata": {
                "type": "overall_summary",
                "file_name": data["file_name"],
                "period_start": llm.get("period_start"),
                "period_end": llm.get("period_end")
            }
        }]