from ..typing.building import building_table,BuildingCreate,BuildingInDB
from ..app import app
from ..data import db
from ..typing.create_data import create_building

@app.post("/building/create_building")
async def createbuilding(
	building:int,
):
	obj=create_building(building)
	obj=BuildingInDB.parse_obj(obj)
	await db.execute(building_table.insert(obj.dict()))
	return {'msg':'success create building'}