from typing import Optional

from fastapi import Depends, HTTPException, status
from ..typing.student import StudentInDB
from ..data import db
from .student import get_is_student
from ..typing.move_in import MoveInDB,MoveInType,move_in_table
from datetime import datetime
from ..typing.create_data import create_id


def CreateMoveIn(stu_id:str)->MoveInDB:
	obj=MoveInDB(
		m_id=create_id(15),
		s_id=stu_id,
		move_in_time=f"{datetime.utcnow()}",
		move_in_status=MoveInType.waiting,
	)
	return obj


async def get_is_studentLive(
	student:StudentInDB=Depends(get_is_student)
)->str:
	try:
		assert student.live_status=="no"
	except:
		raise HTTPException(
			status_code=status.HTTP_400_BAD_REQUEST,
			detail="you already live a dormitory, don't make a joke"
		)
	else:
		obj=CreateMoveIn(student.s_id)
		await db.execute(move_in_table.insert(obj.dict()))
		return "yes"



