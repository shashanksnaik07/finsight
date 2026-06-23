from openai import OpenAI
from dotenv import load_dotenv
import json
import os

load_dotenv()

class StructuredExtractor:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def extract(self, document: dict) -> dict:
        raw_text = document["raw_text"]
        tables = document["tables"]

        print("Extracting structured data...")

        transactions = self._extract_transactions(raw_text, tables)
        summary = self._extract_summary(raw_text)
        metadata = self._extract_metadata(raw_text)

        return {
            "file_name": document["file_name"],
            "metadata": metadata,
            "summary": summary,
            "transactions": transactions
        }

    def _extract_transactions(self, raw_text: str, tables: list) -> list:
        table_text = ""
        if tables:
            for t in tables:
                for row in t["data"]:
                    table_text += " | ".join([str(c) for c in row if c]) + "\n"

        prompt = f"""
        Extract all financial transactions from this document.
        Return ONLY a JSON array. No explanation, no markdown, just raw JSON.

        Each transaction must have:
        - date (string)
        - description (string)
        - amount (float, always positive)
        - type ("debit" or "credit")
        - category (one of: "food", "transport", "utilities", "entertainment", 
                   "shopping", "health", "rent", "salary", "subscription", "other")

        Document text:
        {raw_text}

        Table data:
        {table_text if table_text else "None"}

        Return only the JSON array, nothing else.
        """

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )

        raw = response.choices[0].message.content.strip()
        raw = raw.replace("```json", "").replace("```", "").strip()

        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            print("Warning: Could not parse transactions JSON")
            return []

    def _extract_summary(self, raw_text: str) -> dict:
        prompt = f"""
        Extract the financial summary from this document.
        Return ONLY a JSON object. No explanation, no markdown, just raw JSON.

        Include:
        - opening_balance (float or null)
        - closing_balance (float or null)
        - total_credits (float or null)
        - total_debits (float or null)
        - period_start (string or null)
        - period_end (string or null)

        Document text:
        {raw_text}

        Return only the JSON object, nothing else.
        """

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )

        raw = response.choices[0].message.content.strip()
        raw = raw.replace("```json", "").replace("```", "").strip()

        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            print("Warning: Could not parse summary JSON")
            return {}

    def _extract_metadata(self, raw_text: str) -> dict:
        prompt = f"""
        Extract document metadata from this financial document.
        Return ONLY a JSON object. No explanation, no markdown, just raw JSON.

        Include:
        - document_type (e.g. "bank_statement", "tax_return", "pay_stub", "investment_report")
        - account_holder (string or null)
        - account_number (string or null, mask if present e.g. XXXX-1234)
        - bank_name (string or null)
        - currency (string, e.g. "USD")

        Document text:
        {raw_text}

        Return only the JSON object, nothing else.
        """

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )

        raw = response.choices[0].message.content.strip()
        raw = raw.replace("```json", "").replace("```", "").strip()

        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            print("Warning: Could not parse metadata JSON")
            return {}