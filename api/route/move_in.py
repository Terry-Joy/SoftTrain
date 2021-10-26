from sqlalchemy import and_
from fastapi import Depends,HTTPException,status
from ..typing.move_in import MoveInType,MoveInDB
from ..depends.move_in import get_is_studentLive,move_in_table
from ..app import app
from ..depends.dorm_adminstrator import get_is_Alldormintory_admin
from typing import Optional
from ..typing.building import building_table
from ..typing.student import student_table,StudentInDB
from ..data import db
from ..typing.building import BuildingInDB
from ..typing.dormitory import dormitory_table,DormitoryRoomInDB


@app.get("/move_in/apply_for_move_in")
async def handle_apply_for_move_in(
    apply:Optional[str]=Depends(get_is_studentLive)
):
    return {"msg":"you have applied successfully"}

async def update_move_in(
    
)->:


#change room state
async def is_room_available(
    building_id:str,s_id:str
)->bool:
    obj=await db.fetch_one(dormitory_table.select(and_(
            dormitory_table.c.bel_b_name==building_id,
            dormitory_table.c.Capcity>0
        )))
    if obj:
        obj=DormitoryRoomInDB.parse_obj(obj)
        num=obj.Capcity-1
        await db.execute(dormitory_table.update(
            dormitory_table.c.room_id==obj.room_id,
            {'Capcity':num}
        ))
        await db.execute(student_table.update(
            student_table.c.s_id==s_id,
            {'bel_d_number',obj.room_name}
        ))
        return 1
    else: 
        return 0 



async def alternative_move_in(
    sex:str,s_id:str
):
    obj2=await db.fetch_one(building_table.select(
        building_table.c.sex==sex,        
    ))
    obj2=BuildingInDB.parse_obj(obj2)
    if is_room_available(obj2.building_id):
        await db.execute(student_table.update(
            student_table.c.s_id==s_id,
            {'bel_b_name',obj2.building_id}
        ))
        return 2
    else:
        return 0


#find building 
async def is_student_move_in(
    sex:str,school:str,s_id:str
)->int:#0/1/2 no building,correct,not correct
    obj=await db.fetch_one(building_table.select(and_(
        building_table.c.sex==sex,
        building_table.c.school==school,
    )))        
    obj=BuildingInDB.parse_obj(obj)
    if is_room_available(obj.building_id):
        await db.execute(student_table.update(
            student_table.c.s_id==s_id,
            {'bel_b_name',obj.building_id}
        ))
        return 1        
    elif alternative_move_in(sex,s_id):
        return 2
    else: 
        return 0



@app.get("/move_in/accecp_for_move_in")
async def accpet_for_move_in(
    m_id:str,is_allAdmin:Optional[str]=Depends(get_is_Alldormintory_admin)
):
    obj=await db.fetch_one(move_in_table.select(move_in_table.c.m_id==m_id))
    obj=MoveInDB.parse_obj(obj)
    try:
        assert obj
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Don't exist this apply"
        )
    else:
        obj2=await db.fetch_one(student_table.select(student_table.c.s_id==obj.s_id))
        obj2=StudentInDB.parse_obj(obj2)
        if is_student_move_in(obj2.sex,obj2.school,obj.s_id):
            await db.execute(move_in_table.update(
                move_in_table.c.m_id==m_id,
                {'move_in_status':MoveInType.success}
            ))
            return {"msg":"you have successfully move in"}
        else:
            await db.execute(move_in_table.update(
                move_in_table.c.m_id==m_id,
                {'move_in_status':MoveInType.failed}
            ))   
            return {"msg":"sorry, there is no empty room to move in"}