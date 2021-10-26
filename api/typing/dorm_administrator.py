from sqlalchemy import Column,Table,INTEGER,CHAR,VARCHAR
from sqlalchemy.sql.expression import null
from ..data import meta

from pydantic import BaseModel
from typing import Optional

dorm_administrator_table=Table(
    'dorm_administrator',meta,
    Column(
        'dorm_administrator_id',CHAR(60),
        primary_key=True,
        nullable=False,
        unique=True,
    ),
    Column(
        'd_ad_name',CHAR(60),
        nullable=False,
    ),
    Column(
        'sex',CHAR(50),
        nullable=False,
    ),
    Column(
        'bel_b_id',CHAR(60),
        nullable=True,
    )
)

class Dorm_AdministratorInDB(BaseModel):
    dorm_administrator_id:str
    d_ad_name:str
    sex:str
    bel_b_id:str