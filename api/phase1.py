from fastapi import APIRouter, UploadFile, File
import shutil
import os

from graph.phase1_graph import phase1_graph


router = APIRouter(
    prefix="/api/phase1",
    tags=["Phase 1 - Data Understanding"]
)


@router.post("/analyze")
async def analyze_dataset(file: UploadFile = File(...)):

    # Create data directory
    os.makedirs("data", exist_ok=True)

    # Save uploaded file
    file_path = os.path.join("data", file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Run Phase 1 through LangGraph
    result = phase1_graph.invoke({
        "file_path": file_path,
        "report": ""
    })

    return {
        "status": "success",
        "filename": file.filename,
        "phase": "Phase 1 - Data Understanding",
        "report": result["report"]
    }