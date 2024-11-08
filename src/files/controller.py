from fastapi import File
from sqlalchemy.orm import Session
from .db_model import Files_db
from config import AWS_S3_BUCKET, AWS_S3_ZONE
from files.exceptions import  UnsuportedFileTypeException
from uuid import uuid4
from services.s3_service import s3_upload


async def upload_file(file: File, comment:str, user:str, db:Session, supported_file:str = None) -> Files_db | str:
    """supported_file_type accepts 'images' and 'documents'"""
    
    content = await file.read()
    folder = suported_file_type(file.filename)
    
    if (supported_file != None) and (folder != supported_file):
        raise UnsuportedFileTypeException()
    
    query = Files_db()
    query.comment = comment
    query.ext = file.filename.split('.')[-1].lower()
    query.name = f'{uuid4()}.{query.ext}'
    query.folder = folder
    query.path = f'https://s3.{AWS_S3_ZONE}.amazonaws.com/{AWS_S3_BUCKET}/{folder}/{query.name}'
    query.size = file.size
    query.created_by = user.uuid
    
    print(user)
    
    await s3_upload(contents = content, key = f"{folder}/{query.name}", Content_Type=file.content_type)
    
    db.add(query)
    db.commit()
    db.refresh(query)

    return query

supported_img_filetypes = ['img', 'jpeg', 'jpg', 'png', 'bmp']
supported_document_filetypes = ['doc', 'docx', 'pdf', 'xlsx', 'pptx']

def suported_file_type(filename:str):

    type = filename.split(".")[-1]

    if type.lower() in supported_img_filetypes:
        return 'images'
    elif type.lower() in supported_document_filetypes:
        return 'documents'
    else:
        raise UnsuportedFileTypeException()
