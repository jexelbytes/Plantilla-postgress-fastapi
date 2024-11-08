from fastapi import APIRouter, Request, UploadFile, File
from fastapi import Depends
from sqlalchemy.orm import Session
from database import get_db
from .db_model import ActiveSession_tb
from .authentication import jwtBearer, refresh, user_representation, search_user_controller
from .schemas import auth_sch, refresh_sch, FirebaseToken, UpdateUser
from datetime import datetime
from .controllers.users import update_user_controller, loggin_app_controller, update_user_password_controller, forgot_my_password_controller, update_firebase_token_controller, create_avatar_controller
from .controllers.google import login_google_controller
from .db_model import User_tb
from basic_controller import put_generic_controller
user_router = APIRouter()

@user_router.post("/auth/login")
def login_app(auth:auth_sch, db:Session = Depends(get_db)): return loggin_app_controller(auth=auth, db=db)

@user_router.post("/auth/google")
def login_google(request:Request, db:Session = Depends(get_db)): return login_google_controller(request=request, db=db)

@user_router.post("/auth/refresh")
def login_app(refresh_token:refresh_sch, db:Session = Depends(get_db)):
    return refresh(refresh_token.token, db=db)

@user_router.post("/auth/logout")
def logout_app(db:Session = Depends(get_db), session:ActiveSession_tb = Depends(jwtBearer())):
    session.logout_at = datetime.now()
    db.add(session)
    db.commit()
    return "logged out."

@user_router.get("/my_profile")
def my_profile(user:User_tb = Depends(jwtBearer(get_user=True)), db:Session = Depends(get_db)):
    return user_representation(user=user, db=db)

@user_router.put("/my_profile")
def update_user(
        put_user:UpdateUser,
        db:Session = Depends(get_db),
        user:User_tb = Depends(jwtBearer(get_user=True))
    ): 
    return put_generic_controller(
        db=db,
        db_model=User_tb,
        uuid=user.uuid,
        update_schema=put_user,
        representation_function=user_representation
    )

@user_router.put("/my_profile/password")
def update_user_password(
        db:Session = Depends(get_db),
        user:User_tb = Depends(jwtBearer(get_user=True))
    ):
    return update_user_password_controller(
        user=user,
        db=db
    )
    
@user_router.put("/my_profile/firebase_token")
def update_firebase_token(
        firebase_token:FirebaseToken,
        db:Session = Depends(get_db),
        session:ActiveSession_tb = Depends(jwtBearer())
    ): 
    return update_firebase_token_controller(
        firebase_token=firebase_token,
        session=session,
        db=db
    )

@user_router.put("/my_profile/forgot_my_password")
def forgot_my_password(email:str, db:Session = Depends(get_db)):
    return forgot_my_password_controller(email=email, db=db)

@user_router.post('/my_profile/avatar')
async def create_avatar(user:User_tb = Depends(jwtBearer(get_user=True)), file:UploadFile = File(...), db:Session = Depends(get_db)):
    return await create_avatar_controller(file=file, db=db, user=user)

@user_router.get("/search_another_user", dependencies=[Depends(jwtBearer())])
def search_user(uuid:str, db:Session = Depends(get_db)): return search_user_controller(uuid=uuid, db=db)
