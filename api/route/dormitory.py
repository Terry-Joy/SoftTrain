from ..typing.dormitory import DormitoryRoomInDB,DormitoryRoomCreate,dormitory_table
from ..app import app
from ..data import db
from ..typing.create_data import create_bel_d_number,create_id


# async def update_




@app.post("/dormitory/create_dormitory")
async def create_dormitory(building_id:int,room_name:str):
	obj=DormitoryRoomInDB(
		room_id=create_id(),
		room_name=room_name,
		Capcity=4,
		bel_b_name='C'+f"{building_id}"	
	)
	await db.execute(dormitory_table.insert(obj.dict()))
	return {'msg':'success create dormitory room'}

