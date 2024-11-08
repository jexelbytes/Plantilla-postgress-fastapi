from fastapi import HTTPException

class DebugUnauthorizedException(Exception):
    def __init__(self):
        raise HTTPException(status_code=403, detail="Unauthorized.")