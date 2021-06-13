from sqlalchemy import Column,Table,INTEGER,CHAR,VARCHAR
from sqlalchemy.sql.expression import null
from ..data import meta
from pydantic import BaseModel

table=Table(
    'user',meta,
    Column(
        'U_ID',CHAR(60),
        primary_key=True,
        autoincrement=True,
        nullable=False,
        unique=True,
    ),
    Column(
        'password',CHAR(60),
        nullable=False
    ),
    Column(
        'u_status',CHAR(60),
        nullable=False,
    ),
)

class UserBase(BaseModel):
	uid:str

class UserInDB(UserBase):
	hash_pwd:str