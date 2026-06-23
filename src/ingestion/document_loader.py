import fitz  # PyMuPDF
import pdfplumber
import pytesseract
from pathlib import Path
from pdf2image import convert_from_path
from PIL import Image
import json
import os

class DocumentLoader:
    def __init__(self):
        self.supported_formats = ['.pdf', '.png', '.jpg', '.jpeg']

    def load(self, file_path: str) -> dict:
        path = Path(file_path)
        
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        if path.suffix.lower() not in self.supported_formats:
            raise ValueError(f"Unsupported format: {path.suffix}")

        print(f"Loading: {path.name}")

        if path.suffix.lower() == '.pdf':
            return self._load_pdf(path)
        else:
            return self._load_image(path)

    def _load_pdf(self, path: Path) -> dict:
        # Try text extraction first
        text_content = self._extract_text_pymupdf(path)
        tables = self._extract_tables_pdfplumber(path)
        
        # If text is too short, it's likely a scanned PDF — use OCR
        is_scanned = len(text_content.strip()) < 100
        
        if is_scanned:
            print("Scanned PDF detected — running OCR...")
            text_content = self._ocr_pdf(path)

        return {
            "file_name": path.name,
            "file_type": "pdf",
            "is_scanned": is_scanned,
            "raw_text": text_content,
            "tables": tables,
            "page_count": self._get_page_count(path)
        }

    def _load_image(self, path: Path) -> dict:
        print("Image detected — running OCR...")
        image = Image.open(path)
        text = pytesseract.image_to_string(image)
        
        return {
            "file_name": path.name,
            "file_type": "image",
            "is_scanned": True,
            "raw_text": text,
            "tables": [],
            "page_count": 1
        }

    def _extract_text_pymupdf(self, path: Path) -> str:
        doc = fitz.open(path)
        full_text = ""
        for page in doc:
            full_text += page.get_text()
        doc.close()
        return full_text

    def _extract_tables_pdfplumber(self, path: Path) -> list:
        tables = []
        with pdfplumber.open(path) as pdf:
            for page_num, page in enumerate(pdf.pages):
                page_tables = page.extract_tables()
                for table in page_tables:
                    if table:
                        tables.append({
                            "page": page_num + 1,
                            "data": table
                        })
        return tables

    def _ocr_pdf(self, path: Path) -> str:
        images = convert_from_path(path)
        full_text = ""
        for i, image in enumerate(images):
            print(f"  OCR page {i+1}/{len(images)}...")
            full_text += pytesseract.image_to_string(image)
        return full_text

    def _get_page_count(self, path: Path) -> int:
        doc = fitz.open(path)
        count = doc.page_count
        doc.close()
        return count