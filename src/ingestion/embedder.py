from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct
from openai import OpenAI
from dotenv import load_dotenv
import os
import uuid

load_dotenv()

class Embedder:
    def __init__(self):
        self.openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.qdrant = QdrantClient(host="localhost", port=6333)
        self.collection_name = "finsight"
        self.vector_size = 1536
        self._ensure_collection()

    def _ensure_collection(self):
        existing = [c.name for c in self.qdrant.get_collections().collections]
        if self.collection_name not in existing:
            self.qdrant.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=self.vector_size,
                    distance=Distance.COSINE
                )
            )
            print(f"Created Qdrant collection: {self.collection_name}")

    def embed_chunks(self, chunks: list) -> int:
        print(f"Embedding {len(chunks)} chunks...")
        points = []

        for chunk in chunks:
            response = self.openai.embeddings.create(
                model="text-embedding-3-small",
                input=chunk["text"]
            )
            vector = response.data[0].embedding

            points.append(PointStruct(
                id=str(uuid.uuid4()),
                vector=vector,
                payload={
                    "text": chunk["text"],
                    **chunk["metadata"]
                }
            ))

        self.qdrant.upsert(
            collection_name=self.collection_name,
            points=points
        )

        print(f"Stored {len(points)} vectors in Qdrant")
        return len(points)

    def embed_query(self, query: str) -> list:
        response = self.openai.embeddings.create(
            model="text-embedding-3-small",
            input=query
        )
        return response.data[0].embedding