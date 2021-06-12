from typing import Optional

from fastapi import HTTPException,status

from ..app import app
from ..data import db
from sqlalchemy import select
from ..typing.user import table

async def authenticate(name:str,password:str):
    try:
        obj= await db.fetch_one(select[table,].where(table.c.U_ID==name and table.c.password==password))
        assert obj
        
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User name or Password wrong",
            headers={'WWW-Authenticate':"Bearer"}
        )	
	
	else:


