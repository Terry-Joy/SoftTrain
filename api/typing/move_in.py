from sqlalchemy import Column,Table,INTEGER,CHAR,VARCHAR,ForeignKey,Time
from sqlalchemy.sql.expression import null
from ..data import meta
from typing import Optional
from pydantic import BaseModel
from enum import Enum

move_in_table=Table(
    'move_in_information',meta,
    Column('m_id',CHAR(60),
        primary_key=True,
        nullable=False,
        unique=True,
    ),
    Column('s_id',CHAR(60),
        ForeignKey('student.s_id'),
        nullable=False,
    ),
    Column('move_in_time',CHAR(60),
        nullable=False,
    ),
    Column('move_in_status',CHAR(60),
        nullable=False,
    ),
    Column('move_in_b_name',CHAR(60),
        nullable=True,
    ),
    Column('move_in_d_number',CHAR(60),
        nullable=True,
    ),
)


class MoveInType(str,Enum):
    waiting="待审批"
    success="已分配"
    failed="分配失败"


class MoveInDB(BaseModel):
    m_id:str
    s_id:str
    move_in_time:str
    move_in_status:MoveInType
    move_in_b_name:Optional[str]
    move_in_d_number:Optional[str] 


class MoveCreate(BaseModel):
    m_id:str
    s_id:str
    move_in_time:str
    move_in_status:MoveInType
    move_in_b_name:Optional[str]
    move_in_d_number:Optional[str] 
