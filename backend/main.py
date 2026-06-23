from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routers import documents, query

app = FastAPI(
    title="FinSight API",
    description="Personal Financial Document Intelligence Assistant",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(documents.router, prefix="/api", tags=["documents"])
app.include_router(query.router, prefix="/api", tags=["query"])

@app.get("/")
async def root():
    return {"message": "FinSight API is running"}

@app.get("/health")
async def health():
    return {"status": "healthy"}