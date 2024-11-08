from sqlalchemy import Column, ForeignKey
from sqlalchemy.sql.sqltypes import *
from sqlalchemy.orm import relationship, Mapped
from sqlalchemy.sql import func
from uuid import uuid4
from database import Base

class User_tb(Base):
    __tablename__ = "users"

    uuid = Column(UUID(as_uuid=True), primary_key=True, nullable=False, unique=True, index=True, default=uuid4)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    
    email = Column(String, unique=True, nullable=False)
    phone = Column(String, nullable=True)
    
    hashed_password = Column(String, nullable=False)
    
    avatar = Column(Integer, ForeignKey('files.id'), nullable=True)
    
    created_at = Column(DateTime, nullable=False, default=func.now())
    deleted_at = Column(DateTime, nullable=True)

class ActiveSession_tb(Base):
    __tablename__ = "active_session"
        
    token = Column(String, primary_key=True, nullable=False, unique=True, index=True)
    firebase_token = Column(String, nullable=True)
    user_uuid = Column(UUID(as_uuid=True), ForeignKey('users.uuid'), nullable=False, index=True)
    expire_at = Column(DateTime, nullable=False)
    logout_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, nullable=False, default=func.now())
    
    user_ref: Mapped['User_tb'] = relationship(User_tb)
    
    