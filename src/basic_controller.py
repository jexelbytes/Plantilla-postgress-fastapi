from sqlalchemy.orm import Session
from sqlalchemy import desc, asc
from database import Base
from datetime import datetime, date
from pydantic import BaseModel
from fastapi import HTTPException
import math

def representation_basic(row:Base, db:Session):
    return row.__dict__

def get_generic_controller(db:Session, db_model:Base, size:int, page:int, query_params:dict = {}, order_query:dict = {}, representation_function = representation_basic):
    
    query = db.query(db_model).filter(db_model.deleted_at == None)
    
    for attr, value in query_params.items():
        
        if attr in ("id", "uuid"):
            return representation_function(query.filter(getattr(db_model, attr) == value).first(), db)
        
        elif type(value) == str:
            if ("uuid" in attr) or ("id" in attr):
                query = query.filter(getattr(db_model, attr) == value)
            else:
                query = query.filter(getattr(db_model, attr).icontains(value))
            
        elif type(value) in (bool, int, float, date, datetime):
            query = query.filter(getattr(db_model, attr) == value)
        else:
            try:
                query = query.filter(getattr(db_model, attr) == value)
            except:
                pass
    
    if order_query != {}:
        for attr, value in order_query.items():
            if value == "desc":
                query = query.order_by(desc(getattr(db_model, attr)))
            else:
                query = query.order_by(asc(getattr(db_model, attr)))
    
    querycount = query.count()
    
    query = query.limit(size).offset(page*size).all()
    
    for item in query:
        item = representation_function(item, db)
    
    return {
        'pages':    math.ceil(querycount/size),
        'items':    querycount,
        'data':     query
    }

def post_generic_controller(db:Session, db_model:Base, create_schema:BaseModel, created_by:str = None):
    new_row = db_model(**create_schema.model_dump())
    if created_by:
        new_row.created_by = created_by
    
    db.add(new_row)
    db.commit()
    db.refresh(new_row)
    return new_row

def put_generic_controller(db:Session, db_model:Base, uuid:str, update_schema:BaseModel, representation_function = representation_basic):
    query = db.query(db_model).filter(db_model.deleted_at == None).filter(db_model.uuid == uuid).first()
    
    if not query:
        raise RowNotFoundException(tablename=db_model.__tablename__)
    
    data = update_schema.model_dump(exclude_none=True)
    
    if data.items().__len__() < 1:
        raise EmptyUpdateQueryException()
    
    for key, value in data.items():
        setattr(query, key, value)
    
    db.add(query)
    db.commit()
    db.refresh(query)
    
    return representation_function(query, db)

def delete_generic_controller(db:Session, db_model:Base, uuid:str):
    query = db.query(db_model).filter(db_model.deleted_at == None).filter(db_model.uuid == uuid).first()
    
    if query:
        query.deleted_at = datetime.now()
        db.add(query)
        db.commit()
        db.refresh(query)
    else:
        raise RowNotFoundException(tablename=db_model.__tablename__)
    
    return query

class RowNotFoundException(Exception):
    def __init__(self, tablename:str):
        raise HTTPException(status_code=404, detail=f"{tablename} not found.")
    
class EmptyUpdateQueryException(Exception):
    def __init__(self):
        raise HTTPException(status_code=400, detail=f"Update query is empty.")