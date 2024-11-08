from fastapi import Request, HTTPException
from urllib.parse import urlencode
from config import GOOGLE_OAUTH2_CLIENT_ID, GOOGLE_OAUTH2_CLIENT_SECRET, REDIRECT_URI
from ..db_model import User_tb
from sqlalchemy.orm import Session
from .users import hash_password, login
from services.emails import send_simple_mail_task
import requests
import random

def login_google_controller(request:Request, db:Session):
    request = request.json()
    
    code = request.get("code")
    error = request.get("error")

    if error or not code:
        raise HTTPException(status_code=400, detail="error or not code.")

    redirect_uri = REDIRECT_URI

    access_token = google_get_access_token(code=code, redirect_uri=redirect_uri)
    user_data = google_get_user_info(access_token=access_token)

    user = user_get_or_create(data=user_data, db=db)

    if not user:
        raise HTTPException(detail="UNAUTHORIZED (user not found or invalid)", status_code=401)
        
    return login(user=user, db=db, firebase_token=request.get("firebase_token"))

GOOGLE_ACCESS_TOKEN_OBTAIN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USER_INFO_URL = "https://www.googleapis.com/oauth2/v3/userinfo"

def google_get_access_token(code: str, redirect_uri: str) -> str:
    try:
        # Reference: https://developers.google.com/identity/protocols/oauth2/web-server#obtainingaccesstokens
        data = {
            "code": code,
            "client_id": GOOGLE_OAUTH2_CLIENT_ID,
            "client_secret": GOOGLE_OAUTH2_CLIENT_SECRET,
            "redirect_uri": redirect_uri,
            "grant_type": "authorization_code",
        }
        
        response = requests.post(GOOGLE_ACCESS_TOKEN_OBTAIN_URL, data=data)

        if not response.ok:
            raise HTTPException(status_code=response.status_code, detail=response.json())

        access_token = response.json()["access_token"]

        return access_token
    except Exception as err:
        raise HTTPException(status_code=400, detail=f"{err}")

def google_get_user_info(*, access_token: str):
    # Reference: https://developers.google.com/identity/protocols/oauth2/web-server#callinganapi
    response = requests.get(GOOGLE_USER_INFO_URL, params={"access_token": access_token})
    if not response.ok:
        raise HTTPException(status_code=400, detail="Failed to obtain user info from Google.")
    return response.json()

def user_get_or_create(data, db:Session):
    user = db.query(User_tb).filter(User_tb.email == data.get('email')).first()
    
    email_domain = str(data.get('email')).split('@')[-1].lower()
    
    if not user:
        if email_domain in ("fluxsolar.cl","nextstation.cl","copecflux.cl"):
            user:User_tb = User_tb()
            user.first_name = data.get('given_name')
            user.last_name = data.get('family_name')
            user.email = data.get('email')
            user.hashed_password = hash_password(generate_password(email=user.email))
            db.add(user)
            db.commit()
            db.refresh(user)
    
    return user

def generate_password(email:str, send_mail:bool = True):
    
    avaliable_characters = ['1','2','3','4','5','6','7','8','9','0']
    generated = ""
    for i in range(10):
        generated += avaliable_characters[random.randrange(avaliable_characters.__len__())]
    
    if send_mail:
        send_credentials(email=email, password=generated)
    
    return generated

def send_credentials(email:str, password:str):

    txt = f"""
    Bienvenido a SINAI.
    ------------------------------------------
    Su información de inicio de sesion es:
    
    Usuario: {email}
    
    Contraseña: {password}
    """
    
    send_simple_mail_task(email_receptor=email, content=txt, asunto="Flux login Credentials")
