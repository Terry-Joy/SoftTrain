from sqlalchemy import Column,Table,INTEGER,CHAR,VARCHAR
from sqlalchemy.sql.expression import null
from ..data import meta

from enum import Enum

from pydantic import BaseModel

table=Table(
    'user',meta,
    Column(
        'username',CHAR(60),
        primary_key=True,
        nullable=False,
        unique=True,
    ),
    Column(
        'hash_pwd',CHAR(60),
        nullable=False,
    ),
    Column(
        'usertype',CHAR(60),
        nullable=False,
    ),
)

class UserType(str,Enum):
    student="student"
    dorm_administrator="dorm_administrator"
    system_administrator="system_administrator"

class UserBase(BaseModel):
    username:str


class UserInDB(UserBase):
    hash_pwd:str
    usertype:UserType


class UserCreate(BaseModel):
    user_name:str	
    password:str
    user_type:UserType

