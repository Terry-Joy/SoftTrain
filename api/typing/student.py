from sqlalchemy import Column,Table,INTEGER,CHAR,VARCHAR
from sqlalchemy.sql.expression import null
from ..data import meta

from pydantic import BaseModel

student_table=Table(
    'student',meta,
    Column(
        's_id',CHAR(60),
        primary_key=True,
        nullable=False,
        unique=True,
    ),
    Column(
        'sname',CHAR(60),
        nullable=False,
    ),
    Column(
        'sex',CHAR(50),
        nullable=False,
    ),
    Column(
        'school',CHAR(60),
        nullable=True,
    ),
    Column(
        'grade',INTEGER,
        nullable=False,
    ),
    Column(
        'now_class',INTEGER,
        nullable=True
    ),
    Column(
        'live_status',CHAR(50),
        nullable=False
    ),
    Column(
        'phone_number',CHAR(50),
        nullable=False,
        unique=True,
    ),
    Column(
        'bel_b_name',CHAR(50),
        nullable=True
    ),
    Column(
        'bel_d_number',CHAR(50),
        nullable=True
    ),
)

class StudentInDB(BaseModel):
    s_id:str 
    sname:str 
    sex:str 
    school:str 
    grade:int 
    now_class:int 
    live_status:str
    phone_number:str
    bel_b_name:str
    bel_d_number:str