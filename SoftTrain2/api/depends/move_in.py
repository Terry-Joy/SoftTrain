from typing import Optional

from fastapi import Depends, HTTPException, status
from ..typing.student import StudentInDB,student_table
from ..data import db
from .student import get_is_student
from ..typing.move_in import MoveInDB,MoveInType,move_in_table
from datetime import datetime
from ..typing.create_data import create_id
from sqlalchemy import select


async def CreateMoveIn(stu_id:str,content:str)->MoveInDB:
    obj=await db.fetch_one(student_table.select(
        student_table.c.s_id==stu_id
    ))
    obj=StudentInDB.parse_obj(obj)
    obj=MoveInDB(
        m_id=create_id(15),
        s_id=stu_id,
        sname=obj.sname,
        move_in_time=f"{datetime.now()}"[:19],
        move_in_status=MoveInType.waiting,
		content=content
    )
    return obj


async def get_is_studentLive(
    student:StudentInDB=Depends(get_is_student)
):
    try:
        assert student.live_status=="no"
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="you already live a dormitory, don't make a joke"
        )
    else:
        obj=await CreateMoveIn(student.s_id)
        await db.execute(move_in_table.insert(obj.dict()))
        return "yes"



