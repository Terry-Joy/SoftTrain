from typing import Optional

from fastapi import Cookie, Depends, HTTPException, status
from .user import get_login_user
from ..typing.student import StudentInDB,student_table
from ..typing.user import UserInDB,UserType
from ..data import db

async def get_is_student(
    user:UserInDB=Depends(get_login_user)
)->StudentInDB:
    try:
        assert user.usertype==UserType.student
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You don't have authonization to do this operation"
        )
    else:
        obj=await db.fetch_one(student_table.select(student_table.c.s_id==user.username))
        obj=StudentInDB.parse_obj(obj)
        return obj

