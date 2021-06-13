from typing import Optional

from fastapi import HTTPException,status,Depends,Response
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm

from passlib.context import CryptContext
from ..app import app
from ..data import db
from sqlalchemy import select
from ..typing.user import table,UserInDB
from ..typing.crypto import Token,jwtToken

pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto")

oauth2_scheme=OAuth2PasswordBearer(tokenUrl="/user/login")

async def authenticate(name:str,pwd:str,response:Response)->Token:
	try:
		obj= await db.fetch_one(select[table,].where(table.c.U_ID==name))
		assert obj   
		user=UserInDB.parse_obj(obj)
		assert pwd_context.verify(pwd,user.hash_pwd)
	except:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND,
			detail="User name or Password wrong",
			headers={'WWW-Authenticate':"Bearer"}
        )	
	else:
		token=jwtToken.get_newjwt(user)
		response.set_cookie('token',token)
		return Token(access_token=token,token_type="bearer")


@app.post("/user/loginform",response_model=Token)
async def login_form(
	response:Response,
	form_data:OAuth2PasswordRequestForm=Depends(),
)->Token:
	return await authenticate(form_data.username,form_data.password,) 

