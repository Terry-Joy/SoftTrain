from sqlalchemy import Column,Table,INTEGER,CHAR,VARCHAR
from sqlalchemy.sql.expression import null
from ..data import meta

from pydantic import BaseModel

move_in_table=Table(
	'move_in_information',meta,
	Column('m_id',CHAR(60),
		primary_key=True,
        nullable=False,
        unique=True,
	),
	Column('s_id',CHAR(60),
		nullable=False
	),
	Column(''
	),
	Column('m_status',CHAR(60),
		nullable=False,
	),
	Column('m_b_name',CHAR(60),
		nullable=True,
	),
	Column('m_d_number',CHAR(60),

	),
)

