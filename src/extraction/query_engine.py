from qdrant_client import QdrantClient
from qdrant_client.models import Filter, FieldCondition, MatchValue
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

class QueryEngine:
    def __init__(self, embedder):
        self.embedder = embedder
        self.qdrant = QdrantClient(host="localhost", port=6333)
        self.openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.collection_name = "finsight"

    def query(self, question: str) -> dict:
        print(f"\nQuery: {question}")

        # Embed the question
        query_vector = self.embedder.embed_query(question)

        # Retrieve top 5 relevant chunks
        results = self.qdrant.query_points(
            collection_name=self.collection_name,
            query=query_vector,
            limit=5
        ).points

        # Build context from retrieved chunks
        context = ""
        sources = []
        for r in results:
            context += f"- {r.payload['text']}\n"
            sources.append({
                "text": r.payload["text"],
                "type": r.payload.get("type"),
                "score": round(r.score, 3) if hasattr(r, 'score') else None
            })

        # Generate answer
        prompt = f"""
        You are a personal financial advisor assistant.
        Answer the user's question using ONLY the provided financial data.
        Be specific, cite exact numbers, and end with one actionable insight.
        Never make up numbers not present in the context.

        Financial Data:
        {context}

        Question: {question}

        Answer:
        """

        response = self.openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )

        answer = response.choices[0].message.content.strip()

        return {
            "question": question,
            "answer": answer,
            "sources": sources
        }