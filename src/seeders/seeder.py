from sqlalchemy.orm import Session
from auth.db_model import User_tb
from auth.authentication import hash_password

def init_s(db:Session):
    
    new = User_tb()
    new.first_name = "admin"
    new.email = "admin@example.com"
    new.hashed_password = hash_password("adminadmin")
    db.add(new)
    db.commit()
    
    pass
    
    
    
    