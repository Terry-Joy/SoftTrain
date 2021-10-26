from starlette.status import HTTP_401_UNAUTHORIZED
from api.route.test import create
from typing import Optional,List

from fastapi import HTTPException,status,Depends,Response
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm

from passlib.context import CryptContext
from ..app import app
from ..data import db
from sqlalchemy import select,and_
from ..typing.user import table,UserInDB,UserCreate,UserType
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
    if obj.live_status=='yes':
        obj.bel_b_name=create_bel_b_name(1,obj.sex,obj.school)
    else:
        obj.bel_b_name=""
        obj.bel_d_number=""
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
        usertype=user.user_type.value,
    )

    await db.execute(table.insert(obj.dict()))
    if user.user_type==UserType.student:
        stu_obj=Create_Student(user.user_name)
        await db.execute(student_table.insert(stu_obj.dict()))
        return {'msg':'success create user'}
    elif user.user_type==UserType.dorm_administrator:
        d_ad_obj=Create_Dorm_Admin(user.user_name)
        await db.execute(dorm_administrator_table.insert(d_ad_obj.dict()))
        return {'msg':'success create dormadmin user'}


@app.post("/user/get_current_user")
async def get_current_user(user:UserInDB=Depends(get_login_user)):
    usertype=user.usertype
    if usertype==UserType.student:
        stu_obj=await db.fetch_one(student_table.select(student_table.c.s_id==user.username))
        return stu_obj		
    elif usertype==UserType.dorm_administrator:
        admin_obj=await db.fetch_one(dorm_administrator_table.select(dorm_administrator_table.c.dorm_administrator_id==user.username))
        return admin_obj


@app.get("/user/dorm_get_student_information",response_model=List[StudentInDB])
async def dorm_get_student_information(
    s_id:Optional[str]=None,
    sname:Optional[str]=None,
    sex:Optional[str]=None,
    school:Optional[str]=None,
    grade:Optional[int]=None,
    now_class:Optional[int]=None,
    phone_number:Optional[str]=None,
    bel_b_name:Optional[str]=None,
    bel_d_number:Optional[str]=None,
    user:UserInDB=Depends(get_login_user)
)->List[StudentInDB]:
    usertype=user.usertype
    if usertype==UserType.student:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="You don't have authorization to get this information"
        )
    else: 
        sel=student_table.select()
        if usertype==UserType.dorm_administrator:
            obj=await db.fetch_one(dorm_administrator_table.select(dorm_administrator_table.c.dorm_administrator_id==user.username))
            obj=Dorm_AdministratorInDB.parse_obj(obj)
            if obj.bel_b_id=="all":
                pass
            else:
                if bel_b_name:
                    if obj.bel_b_id==bel_b_name:
                        pass
                    else:
                        raise HTTPException(
                            status_code=HTTP_401_UNAUTHORIZED,
                            detail="You don't have authorization to get this information"
                        )
                else:
                    sel=sel.where(student_table.c.bel_b_name==obj.bel_b_id)

        if s_id:
            sel=sel.where(student_table.c.s_id==s_id)
        if sname:
            sel=sel.where(student_table.c.sname==sname)
        if sex:
            sel=sel.where(student_table.c.sex==sex)	
        if school:
            sel=sel.where(student_table.c.school==school)
        if grade:				
            sel=sel.where(student_table.c.grade==grade)
        if now_class:
            sel=sel.where(student_table.c.now_class==now_class)
        if phone_number:
            sel=sel.where(student_table.c.phone_number==phone_number)
        if bel_b_name:
            sel=sel.where(student_table.c.bel_b_name==bel_b_name)
        if bel_d_number:
            sel=sel.where(student_table.c.bel_d_number==bel_d_number)
        obj=await db.fetch_all(sel)
        return obj


