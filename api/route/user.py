from api.route.test import create
from typing import Optional

from fastapi import HTTPException,status,Depends,Response
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm

from passlib.context import CryptContext
from ..app import app
from ..data import db
from sqlalchemy import select
from ..typing.user import table,UserInDB,UserCreate
from ..typing.crypto import Token,jwtToken

from ..typing.student import student_table,StudentInDB
from ..typing.create_data import create_name,create_sex,create_grade,create_live_status,create_phone_number
from ..typing.create_data import create_bel_b_name,create_bel_d_number,create_now_class,create_school

from ..depends.user import get_login_user
from ..typing.dorm_administrator import dorm_administrator_table,Dorm_AdministratorInDB


pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto")

oauth2_scheme=OAuth2PasswordBearer(tokenUrl="/user/login")


async def authenticate(name:str,pwd:str,response:Response)->Token:
	try:
		obj= await db.fetch_one(table.select(table.c.username==name))
		assert obj   
		user=UserInDB.parse_obj(obj)
		assert pwd_context.verify(pwd,user.hash_pwd)
	except AssertionError:
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail="User name or Password wrong",
			headers={'WWW-Authenticate':"Bearer"}
        )	
	else:
		token=jwtToken.get_newjwt(user)
		response.set_cookie('token',token)
		return Token(access_token=token,token_type="bearer")


@app.get("/user/login",response_model=Token,tags=['authentication'])
async def login(username:str,password:str,response:Response)->Token:
	return await authenticate(username,password,response)


@app.get("/user/logout")
async def logout(response:Response):
	response.set_cookie('token','',expires=1)
	return {'msg':'logout success'}


@app.post("/token",response_model=Token)
async def login_form(
	response:Response,
	form_data:OAuth2PasswordRequestForm=Depends(),
)->Token:
	return await authenticate(form_data.username,form_data.password,response) 


def Create_Student(sid:str)->StudentInDB:
	obj=StudentInDB(
		s_id=sid,
		sname=create_name(),
		sex=create_sex(),
		school=create_school(),
		grade=create_grade(),
		now_class=create_now_class(),
		live_status=create_live_status(),
		phone_number=create_phone_number(),
		bel_b_name="",
		bel_d_number=create_bel_d_number(),
	)
	obj.bel_b_name=create_bel_b_name(1,obj.sex,obj.school)
	return obj
	

def Create_Dorm_Admin(d_ad_id:str)->Dorm_AdministratorInDB:
	obj=Dorm_AdministratorInDB(
		dorm_administrator_id=d_ad_id,
		d_ad_name=create_name(),
		sex=create_sex(),
		bel_b_id=create_bel_b_name(0)
	)
	return obj


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
	print(obj)
	await db.execute(table.insert(obj.dict()))
	if user.user_type=='学生':
		stu_obj=Create_Student(user.user_name)
		await db.execute(student_table.insert(stu_obj.dict()))
		return {'msg':'success create user'}
	elif user.user_type=='宿管':
		d_ad_obj=Create_Dorm_Admin(user.user_name)
		await db.execute(dorm_administrator_table.insert(d_ad_obj.dict()))
		return {'msg':'success'}


@app.post("/user/get_current_user")
async def get_current_user(user:UserInDB=Depends(get_login_user)):
	usertype=user.usertype
	if usertype=='学生':
		stu_obj=await db.fetch_one(student_table.select(student_table.c.s_id==user.username))
		return stu_obj		
	elif usertype=='宿管':
		admin_obj=await db.fetch_one(dorm_administrator_table.select(dorm_administrator_table.c.dorm_administrator_id==user.username))
		return admin_obj


