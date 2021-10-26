import requests
import random
from datetime import date,datetime

def create_id(num:int)->str:
    data=[]
    for i in range(10):
        data.append(f'{i}')	
    id = ""
    for i in range(num):
        id = id + random.choice(data)
    return id

def create_user():
    url = "http://127.0.0.1:8000/user/user_create"
    username=create_id(12)
    password="123456"
    type = ['dorm_administrator','student']
    usertype = random.choice(type)
    dat = {"user_name": username, "password": password, "user_type": usertype}
    print(dat)
    resp=requests.post(url,json=dat)

def create_building(id:int):
    url="http://127.0.0.1:8000/building/create_building"
    parm={"building":id}
    resp=requests.get(url,params=parm)




if __name__ == "__main__":
    # for i in range(1,53):
    #     create_building(i)
    times = 300
    for i in range(times):
        create_user()
	# for 
    print(datetime.today())
