from ..typing.building import building_table,BuildingCreate,BuildingInDB
from ..app import app
from ..data import db
from ..typing.create_data import create_building
from .dormitory import create_dormitory

@app.get("/building/create_building",tags=['init'])
async def createbuilding(
    building:int,
):
    obj=create_building(building)
    obj=BuildingInDB.parse_obj(obj)
    await db.execute(building_table.insert(obj.dict()))
    await create_dormitory(building)
    return {'msg':'success create building'}