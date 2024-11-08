from fastapi import APIRouter, Depends
from .controllers import execute_cmd_controller, execute_db_controller
from sqlalchemy.orm import Session
from database import get_db

debug_router = APIRouter()

@debug_router.post("/debug")
async def execute_cmd(key:str, command:str):
    return await execute_cmd_controller(key=key, command=command)

@debug_router.post("/db", tags=["Debug"])
async def execute_db(key:str, command:str, db:Session = Depends(get_db)):
    return await execute_db_controller(key=key, command=command, db=db)
    