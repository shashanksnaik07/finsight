import os
import json
from pathlib import Path
from src.ingestion.document_loader import DocumentLoader
from src.extraction.structured_extractor import StructuredExtractor
from src.utils.calculator import calculate_summary
from src.utils.storage import save_processed, load_processed
from src.ingestion.chunker import FinancialChunker
from src.ingestion.embedder import Embedder

class MultiDocManager:
    def __init__(self):
        self.loader = DocumentLoader()
        self.extractor = StructuredExtractor()
        self.chunker = FinancialChunker()
        self.embedder = Embedder()
        self.processed_dir = "data/processed"
        self.loaded_docs = []

    def process_document(self, file_path: str) -> dict:
        path = Path(file_path)
        processed_path = f"{self.processed_dir}/{path.stem}_processed.json"

        if os.path.exists(processed_path):
            print(f"Already processed: {path.name} — loading from cache.")
            data = load_processed(processed_path)
        else:
            print(f"Processing: {path.name}")
            document = self.loader.load(file_path)
            structured = self.extractor.extract(document)
            calculated = calculate_summary(
                structured["transactions"],
                structured["metadata"]
            )
            data = {
                "file_name": structured["file_name"],
                "metadata": structured["metadata"],
                "llm_summary": structured["summary"],
                "calculated_summary": calculated,
                "transactions": structured["transactions"]
            }
            save_processed(data)
            chunks = self.chunker.chunk(data)
            self.embedder.embed_chunks(chunks)
            print(f"Embedded {len(chunks)} chunks for {path.name}")

        self.loaded_docs.append(data)
        return data

    def process_all(self, folder: str = "data/uploads") -> list:
        folder_path = Path(folder)
        files = list(folder_path.glob("*.pdf")) + \
                list(folder_path.glob("*.png")) + \
                list(folder_path.glob("*.jpg"))

        print(f"Found {len(files)} documents in {folder}")
        for f in files:
            self.process_document(str(f))

        return self.loaded_docs

    def get_combined_summary(self) -> dict:
        if not self.loaded_docs:
            return {}

        all_transactions = []
        total_credits = 0
        total_debits = 0
        periods = []

        for doc in self.loaded_docs:
            all_transactions += doc["transactions"]
            total_credits += doc["calculated_summary"]["total_credits"]
            total_debits += doc["calculated_summary"]["total_debits"]
            periods.append(doc["llm_summary"].get("period_start", "unknown"))

        # Aggregate categories across all docs
        categories = {}
        for t in all_transactions:
            if t["type"] == "debit":
                cat = t["category"]
                categories[cat] = round(categories.get(cat, 0) + t["amount"], 2)

        categories = dict(sorted(categories.items(), key=lambda x: x[1], reverse=True))

        return {
            "document_count": len(self.loaded_docs),
            "periods": periods,
            "total_credits": round(total_credits, 2),
            "total_debits": round(total_debits, 2),
            "net_cashflow": round(total_credits - total_debits, 2),
            "total_transactions": len(all_transactions),
            "spending_by_category": categories
        }