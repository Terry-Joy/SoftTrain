from typing import Optional

from fastapi import Cookie, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from ..data import db
from ..typing.crypto import jwtToken
from ..typing.user import table,UserInDB


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
        obj=await db.fetch_one(table.select(table.c.username==username))
        assert obj
        return UserInDB.parse_obj(obj)
    except AssertionError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials, please login",
              headers={"WWW-Authenticate": "Bearer"}	,
        )


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
