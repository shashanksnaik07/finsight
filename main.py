import os
import json
from src.ingestion.document_loader import DocumentLoader
from src.extraction.structured_extractor import StructuredExtractor
from src.utils.calculator import calculate_summary
from src.utils.storage import save_processed, load_processed
from src.ingestion.chunker import FinancialChunker
from src.ingestion.embedder import Embedder
from src.extraction.query_engine import QueryEngine

loader = DocumentLoader()
extractor = StructuredExtractor()
chunker = FinancialChunker()
embedder = Embedder()
engine = QueryEngine(embedder)

processed_path = "data/processed/test_processed.json"

# --- Phase 1 + 2: Load, Extract, Chunk, Embed ---
if not os.path.exists(processed_path):
    print("Processing document...")

    document = loader.load("data/uploads/test.pdf")
    structured = extractor.extract(document)
    calculated = calculate_summary(structured["transactions"], structured["metadata"])

    final = {
        "file_name": structured["file_name"],
        "metadata": structured["metadata"],
        "llm_summary": structured["summary"],
        "calculated_summary": calculated,
        "transactions": structured["transactions"]
    }

    save_processed(final)

    chunks = chunker.chunk(final)
    print(f"Created {len(chunks)} chunks")
    embedder.embed_chunks(chunks)

else:
    print("Document already processed — skipping ingestion.")
    final = load_processed(processed_path)

# --- Phase 2: Query ---
questions = [
    "How much did I spend on food?",
    "What is my biggest expense category?",
    "What is my net cashflow this month?",
    "Am I spending too much on subscriptions?"
]

for q in questions:
    result = engine.query(q)
    print(f"\nQ: {result['question']}")
    print(f"A: {result['answer']}")
    print("-" * 50)