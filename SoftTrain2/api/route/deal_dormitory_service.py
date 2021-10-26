from fastapi import FastAPI,Depends
from datetime import datetime
from ..typing.create_data import create_id,create_phone_number
from ..app import app
from ..data import db
from ..typing.deal_dormitory_service import NoticeInDB,N_information_table
from ..typing.dorm_service import RepairInformationInDB,repair_information_table,RepairInformationType
from ..typing.dorm_service import HandleType
from ..depends.dorm_adminstrator import get_is_dormintory_admin
from typing import Optional,List
from fastapi import HTTPException,status,Depends
from pydantic import BaseModel
from ..typing.dorm_administrator import Dorm_AdministratorInDB
from sqlalchemy import or_

async def check_N_ID(id:str)->bool:
    obj=await db.fetch_one(N_information_table.select(
        N_information_table.c.N_ID==id
    ))
    if obj:
        return True
    else:
        return False

async def get_new_N_ID()->str:
    while True:
        S="N"+create_id(15)
        if await check_N_ID(S):
            continue
        return S


@app.get("/deal_dormitory_service/send_notice",tags=['deal_dormitory_service'])#发布通知
async def send_notice(N_title:str,content:str,
    dorm:Dorm_AdministratorInDB=Depends(get_is_dormintory_admin)
):
    obj=NoticeInDB(
        N_ID=await get_new_N_ID(),
        N_title=N_title,
        write_H_ID=dorm.dorm_administrator_id,#！！！获取当前登录宿管的ID
        write_H_name=dorm.d_ad_name,#！！！获取当前登录宿管的姓名
        seeing_B_ID=dorm.bel_b_id,#！！！获取当前宿管所管楼栋的ID
        content=content,
        publish_time=f"{datetime.now()}"[:19]
    )
    await db.execute(N_information_table.insert(obj.dict()))
    return {"message":"Send the notice successfully."}


@app.get("/deal_dormitory_service/get_notice",tags=['deal_dormitory_service'])#查看通知（宿管）
async def get_notice(dorm:Dorm_AdministratorInDB=Depends(get_is_dormintory_admin)):
    obj=await db.fetch_all(N_information_table.select(
        or_(
            N_information_table.c.seeing_B_ID==dorm.bel_b_id,
            N_information_table.c.seeing_B_ID=='all'
        )
    ))           
    return obj
    #！！！返回当前宿管所管楼栋的所有通知，即返回数据库N_information_table中所有“seeing_B_ID=当前宿管所管楼栋ID”的项


@app.get("/deal_dormitory_service/get_repair",tags=['deal_dormitory_service'])#查看保修单
async def get_repair(
    dorm:Dorm_AdministratorInDB=Depends(get_is_dormintory_admin
))->List[RepairInformationInDB]:
    sel=repair_information_table.select()
    sel=sel.where(repair_information_table.c.repair_status==RepairInformationType.pending)
    if dorm.bel_b_id!="all":
        sel=sel.where(repair_information_table.c.report_from_B_name==dorm.bel_b_id)
    obj=await db.fetch_all(sel)
    return obj


@app.get("/deal_dormitory_service/deal_repair",tags=['deal_dormitory_service'])#处理保修单
async def deal_repair(
    repair_ID:str,repair_status:str,
    dorm:Dorm_AdministratorInDB=Depends(get_is_dormintory_admin)
):                                                         
    try:
        obj=await db.fetch_one(
            repair_information_table.select(
            repair_information_table.c.repair_ID==repair_ID
        ))
        assert obj
    except AssertionError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="not found this record",
        )	
    else:
        if repair_status==HandleType.accept:
            await db.execute(repair_information_table.update(
                repair_information_table.c.repair_ID==repair_ID,
                {'repair_status':RepairInformationType.accepted}
            ))
        elif repair_status==HandleType.refused:
            await db.execute(repair_information_table.update(
                repair_information_table.c.repair_ID==repair_ID,
                {'repair_status':RepairInformationType.rejected} 
            ))
        return {'msg':'update successfully'}