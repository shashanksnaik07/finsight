import os
import json
from src.utils.multi_doc_manager import MultiDocManager
from src.extraction.benchmarker import FinancialBenchmarker
from src.extraction.conversation import ConversationEngine
from src.ingestion.embedder import Embedder
from qdrant_client import QdrantClient

# --- Phase 3: Multi-doc + Benchmarking + Conversation ---
manager = MultiDocManager()
benchmarker = FinancialBenchmarker()
embedder = Embedder()
conversation = ConversationEngine(embedder)
qdrant = QdrantClient(host="localhost", port=6333)

# Process all documents in uploads folder
docs = manager.process_all("data/uploads")

# Combined summary across all docs
combined = manager.get_combined_summary()
print("\n--- COMBINED SUMMARY ---")
print(json.dumps(combined, indent=2))

# Benchmark against 50/30/20 rule
# Use first doc for benchmarking
benchmark = benchmarker.benchmark(docs[0]["calculated_summary"])
print("\n--- 50/30/20 BENCHMARK ---")
print(f"Needs:   {benchmark['needs_pct']}% (target: <50%)")
print(f"Wants:   {benchmark['wants_pct']}% (target: <30%)")
print(f"Savings: {benchmark['savings_pct']}% (target: >20%)")
print(f"Flags: {benchmark['flags']}")
print("\nRecommendations:")
for r in benchmark["recommendations"]:
    print(f"  - {r}")

# --- Conversational Q&A with memory ---
def get_context(query: str, limit: int = 5) -> list:
    vector = embedder.embed_query(query)
    results = qdrant.query_points(
        collection_name="finsight",
        query=vector,
        limit=limit
    ).points
    return [r.payload["text"] for r in results]

print("\n--- CONVERSATIONAL Q&A ---")
print("Type your question or 'quit' to exit, 'reset' to clear history.\n")

while True:
    user_input = input("You: ").strip()
    if user_input.lower() == "quit":
        break
    elif user_input.lower() == "reset":
        conversation.reset()
        continue
    elif not user_input:
        continue

    context = get_context(user_input)
    answer = conversation.chat(user_input, context)
    print(f"FinSight: {answer}\n")