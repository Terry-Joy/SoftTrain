from typing import Optional,List
from fastapi import HTTPException,status,Depends,Response
from pydantic import BaseModel
from sqlalchemy import and_,or_
from ..typing.create_data import create_id
from ..typing.dorm_service import WeInformationInDB,WE_information_table,WeInformationType,HandleType
from ..typing.dorm_service import RepairInformationInDB,repair_information_table,RepairInformationType
from ..typing.deal_dormitory_service import NoticeInDB,N_information_table
from .deal_dormitory_service import get_new_N_ID
from ..app import app
from ..data import db
from ..depends.dormitory_service import get_is_studentLive
from ..typing.student import StudentInDB
from datetime import datetime
from ..depends.dorm_adminstrator import get_is_dormintory_admin
from ..typing.dorm_administrator import Dorm_AdministratorInDB


async def check_WE_ID(id:str)->bool:
    obj=await db.fetch_one(WE_information_table.select(
        WE_information_table.c.WE_ID==id
    ))
    if obj:
        return True
    else:
        return False

async def get_new_WE_ID()->str:
    while True:
        S="WE"+create_id(15)
        if await check_WE_ID(S):
            continue
        return S

async def check_repair_ID(id:str)->bool:
    obj=await db.fetch_one(repair_information_table.select(
        repair_information_table.c.repair_ID==id
    ))
    if obj:
        return True
    else:
        return False

async def get_new_repair_ID()->str:
    while True:
        S="R"+create_id(15)
        if await check_repair_ID(S):
            continue
        return S

'''
class Time(BaseModel):
    year:int=0
    month:int=0
    day:int=0
    hour:int=0
    minute:int=0
    second:int=0

    def set_current_time(self):
        tmp=time.localtime(time.time())
        self.year=tmp.tm_year
        self.month=tmp.tm_mon
        self.day=tmp.tm_mday
        self.hour=tmp.tm_hour
        self.minute=tmp.tm_min
        self.second=tmp.tm_sec
        return self
    
    def day_in_month(self,Year:int,Month:int)->int:
        if Month in (1,3,5,7,8,10,12):
            return 31
        elif Month in (4,6,9,11):
            return 30
        elif Year%400==0 or Year%100!=0 and Year%4==0:
            return 29
        else:
            return 28

    def set_time(self,Year:int,Month:int,Day:int,Hour:int,Minute:int,Second:int)->bool:
        if Year<1000 or Year>9999\
            or Month<1 or Month>12\
            or Day<1 or Day>self.day_in_month(Year,Month)\
            or Hour<0 or Hour>23\
            or Minute<0 or Minute>59\
            or Second<0 or Second>59:
            return False
        self.year=Year
        self.month=Month
        self.day=Day
        self.hour=Hour
        self.minute=Minute
        self.second=Second
        return True

    def get_time_str(self)->str:
        return str("%04d-%02d-%02d %02d:%02d:%02d"%\
            (self.year,self.month,self.day,self.hour,self.minute,self.second))

#测试用的WE_information_InDB对象
testWE=WeInformation_InDB(
    WE_ID=get_new_WE_ID(),
    created_time=Time().set_current_time().get_time_str(),
    W_amount=1.23,
    E_amount=4.56,
    money=7.89,
    paid_from_S_ID="123456"
)

#测试用的repair_information_InDB对象
testR=repair_information_InDB(
    repair_ID=get_new_repair_ID(),
    repair_item="air-conditioner",
    report_from_B_name="C10",
    report_from_D_number="434",
    report_S_name="Coming",
    report_phone_number=create_data.create_phone_number(),
    report_time=Time().set_current_time().get_time_str()
)
'''

@app.get("/dormitory_service/create_WE",tags=['init'])#申请水电缴费
async def create_WE(w_amount:float,e_amount:float,bel_b_name:str,bel_d_number:str):
    obj=WeInformationInDB(#450~550 0.61  25~50 0.4
        WE_ID=await get_new_WE_ID(),
        # created_time=Time().set_current_time().get_time_str(),
        W_amount=w_amount,
        E_amount=e_amount,
        bel_b_name=bel_b_name,
        bel_d_number=bel_d_number,
        money=round(w_amount*0.4+e_amount*0.61,2),
        paid_status=WeInformationType.pending,
    )
    await db.execute(WE_information_table.insert(obj.dict()))   
    return {'msg':"success create we_information"}


@app.get("/dormitory_service/get_we_information",tags=['dormitory_service'])
async def get_we_information(student:StudentInDB=Depends(get_is_studentLive)):
    obj=await db.fetch_all(WE_information_table.select(and_(
                WE_information_table.c.bel_b_name==student.bel_b_name,
                WE_information_table.c.bel_d_number==student.bel_d_number,
                WE_information_table.c.paid_status==WeInformationType.pending
            )
        )
    )
    return obj


@app.get("/dormitory_service/get_all_we_information",tags=['dormitory_service'])
async def get_all_we_information(student:StudentInDB=Depends(get_is_studentLive)):
    obj=await db.fetch_all(WE_information_table.select(and_(
                WE_information_table.c.bel_b_name==student.bel_b_name,
                WE_information_table.c.bel_d_number==student.bel_d_number,
                WE_information_table.c.paid_status==WeInformationType.finished
            )
        )
    )
    return obj


@app.get("/dormitory_service/pay_we",tags=['dormitory_service'])
async def pay_we(we_id:str,student:StudentInDB=Depends(get_is_studentLive)):
    await db.execute(WE_information_table.update(
        WE_information_table.c.WE_ID==we_id,
        { 
            'paid_status':WeInformationType.finished,
            'paid_time':f"{datetime.now()}"[:19],
            'paid_from_S_ID':student.s_id,
        }
    ))  
    return {'msg':'success update'}

'''
@app.get("/dormitory_service/pay_WE")#支付水电费
async def pay_WE(WE_ID:str,status:str):
    obj=testWE#！！！获取水电单号为WE_ID的WE_information_InDB对象
    if status=="Success":   
        obj.paid_status="Completed"
        obj.paid_time=Time().set_current_time().get_time_str()
    elif status=="Fail":
        obj.paid_status="Cancelled"
    #！！！在数据库WE_information中修改obj
    result={"message":"OK: the status is "+obj.paid_status+" now."}
    return result
'''

@app.get("/dormitory_service/create_repair",tags=['dormitory_service'])#申请报修
async def create_repair(phone_number:str,repair_item:str,
    student:StudentInDB=Depends(get_is_studentLive)
):
    obj=RepairInformationInDB(
        repair_ID=await get_new_repair_ID(),
        repair_item=repair_item,
        report_from_B_name=student.bel_b_name,#！！！获取当前登录学生所住的楼栋名称
        report_from_D_number=student.bel_d_number,#！！！获取当前登录学生所住的宿舍号
        report_S_name=student.sname,#！！！获取当前登录学生的姓名
        report_phone_number=phone_number,
        report_time=f"{datetime.now()}"[:19],
        repair_status=RepairInformationType.pending,
    )
    #！！！将obj加入数据库repair_information
    await db.execute(repair_information_table.insert(obj.dict()))
    result={"message":"OK: sumbit successfully."}
    return result

#update 
@app.get("/dormitory_service/see_repair",tags=['dormitory_service'])
async def see_repair(student:StudentInDB=Depends(get_is_studentLive))->List[RepairInformationInDB]:
    obj=await db.fetch_all(repair_information_table.select(and_(
        repair_information_table.c.report_from_B_name==student.bel_b_name,
        repair_information_table.c.report_from_D_number==student.bel_d_number
    )))
    return obj


@app.get("/dormitory_service/see_notice",tags=['dormitory_service'])#查看通知（学生）
async def see_notice(student:StudentInDB=Depends(get_is_studentLive)):
    #测试用的NoticeInDB对象
    obj=await db.fetch_all(
        N_information_table.select(
			or_(
            	N_information_table.c.seeing_B_ID==student.bel_b_name,
				N_information_table.c.seeing_B_ID=='all'
			)
        )
    )
    return obj
    #！！！返回当前学生所住楼栋的所有通知，即返回数据库N_information_table中所有“seeing_B_ID=当前学生所住楼栋ID”的项