import importlib
import pkgutil
from os import path
from fastapi import FastAPI

app=FastAPI(title="soft_homework",)

@app.get('/')
async def root():
    return {'msg':'success'}

modules={}

for name in ['route']:
    for moduleInfo in pkgutil.iter_modules(
        [path.join(path.split(__file__)[0],name)],
            f'api.{name}.',
    ): 
        name=moduleInfo.name
        modules[name]=importlib.import_module(name)

# print(modules)
