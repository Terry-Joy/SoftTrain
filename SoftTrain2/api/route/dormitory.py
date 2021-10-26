from ..typing.dormitory import DormitoryRoomInDB,DormitoryRoomCreate,dormitory_table
from ..app import app
from ..data import db
from ..typing.create_data import create_bel_d_number,create_id


# async def update_

async def create_dormitory(building_id:int):
    for i in range(1,61):
        j=i
        str=f'{j}'
        if len(str)<=1:
            str='0'+str
        str2=['1','2','3','4','5','6','7']
        for k in str2:
            name=k+str
            obj=DormitoryRoomInDB(
                room_id=create_id(),
                room_name=name,
                Capcity=4,
                bel_b_name='C'+f"{building_id}"	
            )
            await db.execute(dormitory_table.insert(obj.dict()))
    return {'msg':'success create dormitory room'}

