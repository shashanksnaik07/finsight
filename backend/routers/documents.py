from fastapi import APIRouter, UploadFile, File, HTTPException
from backend.models.schemas import DocumentResponse
from src.utils.multi_doc_manager import MultiDocManager
from src.extraction.benchmarker import FinancialBenchmarker
import shutil
import os

router = APIRouter()
manager = MultiDocManager()
benchmarker = FinancialBenchmarker()

@router.post("/upload", response_model=DocumentResponse)
async def upload_document(file: UploadFile = File(...)):
    # Validate file type
    allowed = [".pdf", ".png", ".jpg", ".jpeg"]
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in allowed:
        raise HTTPException(status_code=400, detail=f"Unsupported file type: {ext}")

    # Save uploaded file
    upload_path = f"data/uploads/{file.filename}"
    with open(upload_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Process document
    try:
        data = manager.process_document(upload_path)
        benchmark = benchmarker.benchmark(data["calculated_summary"])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return DocumentResponse(
        file_name=data["file_name"],
        metadata=data["metadata"],
        calculated_summary=data["calculated_summary"],
        benchmark=benchmark,
        message="Document processed successfully"
    )

@router.get("/documents")
async def list_documents():
    processed_dir = "data/processed"
    if not os.path.exists(processed_dir):
        return {"documents": []}
    
    files = [f.replace("_processed.json", "") 
             for f in os.listdir(processed_dir) 
             if f.endswith("_processed.json")]
    
    return {"documents": files}