from sqlalchemy import Column, ForeignKey
from sqlalchemy.sql.sqltypes import *
from sqlalchemy.orm import relationship, Mapped, DeclarativeBase, Session
from typing import Optional
from sqlalchemy.sql import func
from uuid import uuid4
from database import Base

class Files_db(Base):
    __tablename__ = "files"
    id = Column(Integer, index=True, primary_key=True, unique=True, autoincrement=True)
    name =                  Column(String, nullable=False)
    comment =               Column(String, nullable=True)
    path =                  Column(String, nullable=False)
    ext =                   Column(String, nullable=False)
    size =                  Column(Integer, nullable=False)
    folder =                Column(String, nullable=False)
    created_by =            Column(UUID(as_uuid=True), nullable=True)
    created_at =            Column(DateTime, default=func.now())
    deleted_at =            Column(DateTime, nullable=True, default=None)