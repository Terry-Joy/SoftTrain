from typing import Optional

from fastapi import HTTPException,status,Depends,Response
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm

from passlib.context import CryptContext
from ..app import app
from ..data import db
from sqlalchemy import select
from ..typing.user import table,UserInDB,UserCreate
from ..typing.crypto import Token,jwtToken

from ..typing.student import student_table


pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto")

oauth2_scheme=OAuth2PasswordBearer(tokenUrl="/user/login")


async def authenticate(name:str,pwd:str,response:Response)->Token:
	try:
		obj= await db.fetch_one(table.select(table.c.username==name))
		assert obj   
		user=UserInDB.parse_obj(obj)
		assert pwd_context.verify(pwd,user.hash_pwd)
	except:
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail="User name or Password wrong",
			headers={'WWW-Authenticate':"Bearer"}
        )	
	else:
		token=jwtToken.get_newjwt(user)
		response.set_cookie('token',token)
		return Token(access_token=token,token_type="bearer")


@app.get("/user/login",response_model=Token)
async def login(username:str,password:str,response:Response)->Token:
	return await authenticate(username,password,response)


@app.get("/user/logout")
async def logout(response:Response):
	response.set_cookie('token','',expires=1)
	return {'msg':'logout success'}


@app.post("/user/loginform",response_model=Token)
async def login_form(
	response:Response,
	form_data:OAuth2PasswordRequestForm=Depends(),
)->Token:
	return await authenticate(form_data.username,form_data.password,response) 


async def Create_Student(sid:str):
	sex=


@app.post("/user/user_create")
async def user_create(
	user:UserCreate
):
	if await db.fetch_val(table.count(table.c.username==user.user_name)):
		raise HTTPException(
			status_code=status.HTTP_400_BAD_REQUEST,
			detail="Username repeat",
		)
	obj=UserInDB(
		username=user.user_name,
		hash_pwd=pwd_context.hash(user.password),
		usertype=user.user_type,
	)
	await db.execute(table.insert(obj.dict()))
	if user.user_type=='学生':

	return {'msg':'success create user'}