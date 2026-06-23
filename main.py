from src.ingestion.document_loader import DocumentLoader
from src.extraction.structured_extractor import StructuredExtractor
from src.utils.calculator import calculate_summary
from src.utils.storage import save_processed
import json

loader = DocumentLoader()
extractor = StructuredExtractor()

# Load + extract
document = loader.load("data/uploads/test.pdf")
structured = extractor.extract(document)

# Calculate programmatically (never trust LLM for math)
calculated = calculate_summary(structured["transactions"], structured["metadata"])

# Merge everything
final = {
    "file_name": structured["file_name"],
    "metadata": structured["metadata"],
    "llm_summary": structured["summary"],       # LLM extracted (dates, balances)
    "calculated_summary": calculated,            # Programmatic (totals, categories)
    "transactions": structured["transactions"]
}

# Save
save_processed(final)

# Print
print("\n--- METADATA ---")
print(json.dumps(final["metadata"], indent=2))

print("\n--- CALCULATED SUMMARY ---")
print(json.dumps(final["calculated_summary"], indent=2))

print("\n--- SPENDING BY CATEGORY ---")
for cat, amount in final["calculated_summary"]["spending_by_category"].items():
    print(f"  {cat}: ${amount}")

print(f"\nTop expense: {final['calculated_summary']['top_expense']}")