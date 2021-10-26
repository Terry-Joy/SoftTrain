from typing import Optional,List
from fastapi import FastAPI,Depends,HTTPException, status
from pydantic import BaseModel
from ..typing.leave_school import LeaveSchoolInformationInDB
from ..typing.student import StudentInDB 
from ..typing.dorm_administrator import Dorm_AdministratorInDB
from ..app import app
from ..depends.dormitory_service import get_is_studentLive
from ..typing.leave_school import leave_school_information_table,LeaveSchoolStatus
from ..typing.leave_school import HandleType
from ..data import db
from ..depends.dorm_adminstrator import get_is_dormintory_admin
from sqlalchemy import and_


@app.get("/leave_school/apply_for_leave_school",tags=['leave_school'])#离校申请
async def apply_leave_school(
    leave_kind:str,leave_reason:Optional[str],leave_date:str,
    student:StudentInDB=Depends(get_is_studentLive)
):
    obj2=await db.fetch_one(leave_school_information_table.select(
                leave_school_information_table.c.leave_S_ID==student.s_id,
            )
        )
    obj=LeaveSchoolInformationInDB(
        leave_S_ID=student.s_id,#！！！获取当前登录学生的ID
        leave_S_name=student.sname,#！！！获取当前登录学生的姓名
        leave_S_bel_B_name=student.bel_b_name,#！！！获取当前登录学生所住的楼栋名称
        leave_S_bel_D_number=student.bel_d_number,#！！！获取当前登录学生所住的宿舍号
        leave_kind=leave_kind,
        leave_reason=leave_reason,
        leave_date=leave_date,
        serve_status=LeaveSchoolStatus.pending,    
    )
    if obj2:
        # return {'msg':'caonima'}
        await db.execute(leave_school_information_table.delete(
            leave_school_information_table.c.leave_S_ID==student.s_id
        ))
    await db.execute(leave_school_information_table.insert(obj.dict()))
    #！！！将obj加入数据库leave_school_information
    result={"message":"OK: sumbit successfully."}
    return result


@app.get('/leave_school/cancel',tags=['leave_school'])
async def leave_school_cancel(
    student:StudentInDB=Depends(get_is_studentLive)
):
    try:
        obj=await db.fetch_one(leave_school_information_table.select(and_(
                    leave_school_information_table.c.leave_S_ID==student.s_id,
                )
            )
        )
        assert obj
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="there is no leave_school_application"
        )
    else:  
        await db.execute(leave_school_information_table.delete(
            leave_school_information_table.c.leave_S_ID==student.s_id
        ))
        return {'msg':'you have calcel this requests'}


@app.get("/leave_school/stu_get_leave_school_information",tags=['leave_school'])
async def stu_get_leave_school(
    student:StudentInDB=Depends(get_is_studentLive)
)->LeaveSchoolInformationInDB:
    obj=await db.fetch_one(leave_school_information_table.select(and_(
                leave_school_information_table.c.leave_S_ID==student.s_id,
            )
        )
    )
    return obj


@app.get("/leave_school/dorm_get_leave_school_information",tags=['leave_school'])
async def dorm_get_leave_school(
    dorm:Dorm_AdministratorInDB=Depends(get_is_dormintory_admin),
)->List[LeaveSchoolInformationInDB]:
    sel=leave_school_information_table.select()
    sel=sel.where(leave_school_information_table.c.serve_status==LeaveSchoolStatus.pending)
    if dorm.bel_b_id!='all':
        sel=sel.where(leave_school_information_table.c.leave_S_bel_B_name==dorm.bel_b_id)
    obj=await db.fetch_all(sel)
    return obj        


@app.get("/leave_school/handle_leave_school",tags=['leave_school'])
async def handle_leave_school(
    leave_S_ID:str,status:str,dorm:Dorm_AdministratorInDB=Depends(get_is_dormintory_admin),
):
    if status==HandleType.accept:
        await db.execute(leave_school_information_table.update(
            and_(
                leave_school_information_table.c.leave_S_ID==leave_S_ID,
                leave_school_information_table.c.serve_status==LeaveSchoolStatus.pending
            ),
            {'serve_status':LeaveSchoolStatus.finished}
        ))
    elif status==HandleType.refused:
        await db.execute(leave_school_information_table.update(
            and_(
                leave_school_information_table.c.leave_S_ID==leave_S_ID,
                leave_school_information_table.c.serve_status==LeaveSchoolStatus.pending
            ),
            {'serve_status':LeaveSchoolStatus.failed}
        ))
    return {'msg':'you have update successfully'}

