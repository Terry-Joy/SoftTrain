from typing import Optional

from fastapi import Cookie, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime,timedelta
from ..data import db
from ..typing.crypto import jwtToken
from ..typing.user import table,UserInDB,UserType
from ..typing.dorm_administrator import Dorm_AdministratorInDB,dorm_administrator_table

oauth2_scheme=OAuth2PasswordBearer(tokenUrl='token',auto_error=False)


async def getToken(
    header_Token:Optional[str]=Depends(oauth2_scheme),
    token:Optional[str]=Cookie(None),
)->str:
    realToken=header_Token or token
    # print(realToken)
    if realToken:
        return realToken
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not find token",
              headers={"WWW-Authenticate": "Bearer"},
        )


async def get_login_user(token:str=Depends(getToken))->UserInDB:
    try:
        username=jwtToken.decode(token).sub
        realtime=jwtToken.decode(token).exp
        assert str(realtime)>=str(datetime.now())           
        obj=await db.fetch_one(table.select(table.c.username==username))
        assert obj
        return UserInDB.parse_obj(obj)
    except AssertionError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials, please login",
              headers={"WWW-Authenticate": "Bearer"}	,
        )



async def get_is_system_or_all_admin(
    user:UserInDB=Depends(get_login_user)
):
    if user.usertype==UserType.system_administrator:
        return user
    elif user.usertype==UserType.dorm_administrator:
        obj=await db.fetch_one(dorm_administrator_table.select(
            dorm_administrator_table.c.dorm_administrator_id==user.username
        ))
        obj=Dorm_AdministratorInDB.parse_obj(obj)
        if obj.bel_b_id=='all':
            return user
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="You don't have authorization to get this information"
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You don't have authorization to get this information"
        )


async def get_is_system_admin(
    user:UserInDB=Depends(get_login_user)
):
    try:
        assert user.usertype==UserType.system_administrator
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You don't have authorization to get this information'"
        )
    return user


# async def login_user_possible(
# 	header_Token:Optional[str]=Depends(oauth2_scheme),
# 	token:Optional[str]=Cookie(None),
# )->Optional[UserInDB]:
# 	try:
# 		realToken=header_Token or token
# 		if realToken:
# 			return await get_login_user(realToken)	
# 	except:
# 		pass
