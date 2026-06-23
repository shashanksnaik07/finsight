import json
from pathlib import Path

def save_processed(data: dict, output_dir: str = "data/processed"):
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    file_name = Path(data["file_name"]).stem
    output_path = Path(output_dir) / f"{file_name}_processed.json"
    
    with open(output_path, "w") as f:
        json.dump(data, f, indent=2)
    
    print(f"Saved: {output_path}")
    return str(output_path)

def load_processed(file_path: str) -> dict:
    with open(file_path, "r") as f:
        return json.load(f)