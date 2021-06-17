from fastapi.datastructures import Default
from sqlalchemy import Column,Table,INTEGER,CHAR,VARCHAR
from sqlalchemy.sql.expression import null
from sqlalchemy.sql.sqltypes import INT
from ..data import meta

from pydantic import BaseModel

dormitory_table=Table(
	'dormitory_room',meta,
	Column(
		'room_id',CHAR(60),
		primary_key=True,
		nullable=True,
		unique=True,
	),
	Column(
		'room_name',CHAR(60),
		nullable=False,
	),
	Column(
		'Capcity',INTEGER,
		nullable=False
	)
)

class dormitory_room_table(BaseModel):
	room_id:str
	room_name:str
	Capcity:INTEGER