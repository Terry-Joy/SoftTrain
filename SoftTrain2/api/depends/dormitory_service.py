from typing import Optional
from fastapi import Depends,HTTPException,status
from ..typing.student import StudentInDB
from ..data import db
from .student import get_is_student

async def get_is_studentLive(
    student:StudentInDB=Depends(get_is_student)
):
    try:
        assert student.live_status=="yes"
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You don't have authorization to get this information"
        )
    else:
        return student