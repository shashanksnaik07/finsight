# FinSight 🔍
AI-powered personal financial document intelligence assistant.

## What it does
Upload your bank statements, tax returns, or pay stubs — FinSight extracts, 
understands, and answers natural language questions about your finances.

## Phase 1 (Complete)
- PDF + scanned document ingestion
- LLM-powered structured extraction (transactions, categories, metadata)
- Programmatic financial calculations (no LLM math)

## Coming Soon
- RAG-powered Q&A over your financial documents
- Cross-document reasoning
- Actionable financial insights

## Tech Stack
- PyMuPDF, pdfplumber, Tesseract OCR
- OpenAI GPT-4o-mini
- LlamaIndex + Qdrant (Phase 2)
- FastAPI + Next.js (Phase 4)