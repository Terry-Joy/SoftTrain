from typing import Optional

from fastapi import Depends,HTTPException, status
from ..typing.create_data import create_id
from ..typing.user import UserInDB,UserType
from .user import get_login_user
from ..typing.dorm_administrator import Dorm_AdministratorInDB,dorm_administrator_table
from ..data import db


async def get_is_dormintory_admin(
    user:UserInDB=Depends(get_login_user)
)->Dorm_AdministratorInDB:
    try:
        assert user.usertype==UserType.dorm_administrator
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You don't have authonization to do this operation"
        )
    else:
        obj=await db.fetch_one(dorm_administrator_table.select(
            dorm_administrator_table.c.dorm_administrator_id==user.username))
        obj=Dorm_AdministratorInDB.parse_obj(obj)
        return obj


async def get_is_Alldormintory_admin(
   dorm_Alladministrator:Dorm_AdministratorInDB=Depends(get_is_dormintory_admin) 
)->str:
    try:
        assert dorm_Alladministrator.bel_b_id=='all'
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You don't have authonization to do this operation"
        )
    else:
        return "yes"

