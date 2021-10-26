from fastapi.datastructures import Default
from sqlalchemy import Column,Table,INTEGER,CHAR,VARCHAR
from sqlalchemy.sql.expression import null
from sqlalchemy.sql.sqltypes import INT
from ..data import meta

from pydantic import BaseModel

building_table=Table(
    'building',meta,
    Column(
        'building_id',CHAR(60),
        primary_key=True,
        nullable=False,
        unique=True,
    ),	
    Column(
        'sex',CHAR(60),
        nullable=False,
    ),
    Column(
        'school',CHAR(60),
        nullable=False,
    )
)


class BuildingCreate(BaseModel):
    building_id:str
    sex:str
    school:str


class BuildingInDB(BaseModel):
    building_id:str
    sex:str
    school:str