from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class auth_sch(BaseModel):
  email: EmailStr
  password: str = Field(min_length=8, max_length=128)
  firebase_token:str | None = None

  model_config = {
    "json_schema_extra": {
      "examples": [{
        "email": "person@email.com",
        "password": "12345678"
      }]
    }
  }
  
class CreateUser(BaseModel):
  first_name: Optional[str] = Field(min_length=1, max_length=128, default=None)
  last_name: Optional[str] = Field(min_length=1, max_length=128, default=None)
  email: EmailStr
  phone: str | None = None
  hashed_password: str = Field(min_length=8, max_length=128)

class UpdateUser(BaseModel):
  first_name: Optional[str] = Field(min_length=1, max_length=128, default=None)
  last_name: Optional[str] = Field(min_length=1, max_length=128, default=None)
  email: EmailStr | None = None
  phone: str | None = None
  hashed_password: str = Field(min_length=8, max_length=128, default=None)

class UpdateUserPassword(BaseModel):
  new_password: str = Field(min_length=8, max_length=128)
  old_password: str = Field(min_length=8, max_length=128)

class refresh_sch(BaseModel):
  token: str
  
class FirebaseToken(BaseModel):
  firebase_token: str
