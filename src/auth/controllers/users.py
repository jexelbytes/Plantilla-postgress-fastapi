from ..exceptions import UserNotFoundException, InvalidCredentialsException, GenericException
from ..authentication import user_representation, hash_password, login
from ..schemas import CreateUser, auth_sch, UpdateUser, FirebaseToken
from ..db_model import User_tb, ActiveSession_tb
from fastapi import Depends
from sqlalchemy.orm import Session
from database import get_db
from sqlalchemy import desc
from services.emails import generate_password
import math
from fastapi import UploadFile
from sqlalchemy.orm import Session
from auth.db_model import User_tb
from files.controller import upload_file


async def create_avatar_controller(file:UploadFile, db:Session, user:User_tb):
    
    file = await upload_file(file=file, comment=None, user=user, db=db, supported_file='images')
    file_id = file.id
    db.refresh(user)
    user.avatar = file_id
    db.add(user)
    db.commit()
    db.refresh(file)
    
    return file

def loggin_app_controller(auth:auth_sch, db:Session = Depends(get_db)):
    
    email = auth.email
    password = auth.password
    
    user = db.query(User_tb).filter(User_tb.email == email).first()
    
    if not user:
        raise InvalidCredentialsException()
    
    if user.hashed_password != hash_password(password=password):
        raise InvalidCredentialsException()
    
    return login(user=user, db=db, firebase_token=auth.firebase_token)

def create_user_controller(new_user:CreateUser, db:Session = Depends(get_db)):
    try:
        new_user = User_tb(**new_user.model_dump())
        new_user.hashed_password = hash_password(new_user.hashed_password)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return user_representation(new_user)
    except Exception as err:
        raise GenericException(err)

def update_user_controller(uuid:str, put_user:UpdateUser, db:Session = Depends(get_db)):
    data = put_user.model_dump(exclude_none=True)
    
    user = search_user_controller(uuid=uuid, db=db)
    
    for key, value in data.items():
        setattr(user, key, value)
        
    db.add(user)
    db.commit()
    db.refresh(user)
    return user_representation(user)

def update_user_password_controller(user:User_tb, db:Session = Depends(get_db)):
    
    new_password = generate_password(user.email)
    
    new_password = hash_password(new_password)
        
    user.hashed_password = new_password
    
    db.add(user)
    db.commit()
    db.refresh(user)
    return user_representation(user)

def update_firebase_token_controller(firebase_token:FirebaseToken, session:ActiveSession_tb, db:Session):
    session.firebase_token = firebase_token.firebase_token
    db.add(session)
    db.commit()
    return "ok"

def forgot_my_password_controller(email:str, db:Session):
    user = db.query(User_tb).filter(User_tb.email == email).first()
    
    if not user:
        raise UserNotFoundException()
    
    return update_user_password_controller(uuid=user.uuid, db=db)

def search_user_controller(uuid:str = None, first_name:str = None, email:str = None, last_name:str = None, rut:str = None, page:int=0, limit:int=100, db:Session = Depends(get_db)):
    search = db.query(User_tb).order_by(desc(User_tb.created_at))
    
    if uuid:
        return search.filter(User_tb.uuid == uuid).first()
    
    if first_name:
        search = search.filter(User_tb.first_name.icontains(first_name))
    
    if last_name:
        search = search.filter(User_tb.last_name.icontains(last_name))
    
    if rut:
        search = search.filter(User_tb.rut.icontains(rut))
        
    if email:
        search = search.filter(User_tb.email.icontains(email))
        
    count = search.count()
    
    return {
        'pages':    math.ceil(count/limit),
        'items':    count,
        'limit':    limit,
        'page':     page,
        'data':     search.limit(limit).offset(page*limit).all()
    }

