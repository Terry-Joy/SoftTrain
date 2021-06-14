from sqlalchemy import Column,Table,INTEGER
from ..data import meta

table=Table(
    'test',meta,
    Column(
        'id',INTEGER,
        primary_key=True,
        autoincrement=True,
    ),
)

