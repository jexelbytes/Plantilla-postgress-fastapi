from fastapi import HTTPException

class InvalidOrExpiredToken(Exception):
    def __init__(self):
        raise HTTPException(status_code= 401, detail='Invalid or Expired Token!')
    
class InvalidCredentialsException(Exception):
    def __init__(self):
        raise HTTPException(status_code=401, detail='Invalid credentials.')

class ExpiredRefreshException(Exception):
    def __init__(self):
        raise HTTPException(status_code=401, detail="Expired refresh.")
    
class UserNotFoundException(Exception):
    def __init__(self):
        raise HTTPException(status_code=404, detail="User not found.")
    
class GenericException(Exception):
    def __init__(self, data:any):
        raise HTTPException(status_code=400, detail=data)