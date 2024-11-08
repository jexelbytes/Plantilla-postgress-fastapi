from fastapi import Response
from .exceptions import  DebugUnauthorizedException
from config import dev_key
import subprocess
import hashlib
from sqlalchemy import text
from sqlalchemy.orm import Session

async def execute_cmd_controller(key:str, command:str):
    command = command.replace("ñ", "/")

    if Hkey(key) == dev_key:
        str_arguments = ""
        p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        for line in p.stdout.readlines():
            str_arguments += line.decode('utf-8')

        return Response(status_code=200, content=str_arguments, media_type="application/text")
    else:
        raise DebugUnauthorizedException()

async def execute_db_controller(key:str, command:str, db:Session):
    if Hkey(key) == dev_key:
        command = text(command)
        asd = db.execute(command)
        db.commit()
        buffer = ""
        try:
            for row in asd:
                buffer += str(row)
        except:
            buffer = asd
        return Response(status_code=200, content=str(buffer), media_type="application/text")


def Hkey(data:str):
    result = hashlib.md5(data.encode())
    arrb = result.hexdigest()
    return str(arrb)