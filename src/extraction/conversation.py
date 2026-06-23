from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

class ConversationEngine:
    def __init__(self, embedder, qdrant_collection="finsight"):
        self.embedder = embedder
        self.openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.collection_name = qdrant_collection
        self.history = []
        self.system_prompt = """
        You are a personal financial advisor assistant.
        Answer questions using ONLY the provided financial data.
        Be specific, cite exact numbers, and give one actionable insight per answer.
        Never make up numbers. If data is not available, say so clearly.
        Keep answers concise — 3-5 sentences max.
        """

    def chat(self, user_message: str, context_chunks: list) -> str:
        # Build context string
        context = "\n".join([f"- {c}" for c in context_chunks])

        # Add user message to history
        self.history.append({
            "role": "user",
            "content": f"Financial Data:\n{context}\n\nQuestion: {user_message}"
        })

        # Call OpenAI with full history for memory
        response = self.openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": self.system_prompt},
                *self.history
            ],
            temperature=0
        )

        answer = response.choices[0].message.content.strip()

        # Store assistant response in history
        self.history.append({
            "role": "assistant",
            "content": answer
        })

        return answer

    def reset(self):
        self.history = []
        print("Conversation reset.")