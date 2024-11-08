from fastapi import HTTPException

class UnsuportedFileTypeException():
    def __init__(self) -> None:
        raise HTTPException(status_code=400, detail=f"Unsuported file type.")