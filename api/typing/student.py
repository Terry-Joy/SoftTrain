from sqlalchemy import Column,Table,INTEGER,CHAR,VARCHAR
from sqlalchemy.sql.expression import null
from ..data import meta

table=Table(
    'student',meta,
    Column(
        'S_ID',CHAR(60),
        primary_key=True,
        autoincrement=True,
        nullable=False,
        unique=True,
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
        'class',int,
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
        'bel_B_name',CHAR(50),
        nullable=True
    ),
    Column(
        'bel_D_number',INTEGER,
        nullable=True
    ),
)