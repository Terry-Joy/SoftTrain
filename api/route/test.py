from ..app import app
from ..data import db
from ..typing.test import table


@app.get('/create')
async def create(id:int):
    await db.execute(table.insert().values(id=id))
    return {'msg':'success'}

@app.get('/all')
async def all():
    return await db.fetchall(table.select())

@app.get('/recreate_db')
async def recreate():
    from ..data import meta
    meta.drop_all()
    meta.create_all()
    return {'msg':'success'}
    