import requests
import random


def create_id(num:int)->str:
	data=[]
	for i in range(10):
		data.append(f'{i}')	
	id = ""
	for i in range(num):
		id = id + random.choice(data)
	return id

def create_user():
	url = "http://127.0.0.1:8080/user/user_create"
	username=create_id(12)
	password=create_id(15)
	type = ['student', 'dorm_administrator','system_administrator']
	usertype = random.choice(type)
	dat = {"user_name": username, "password": password, "user_type": usertype}
	print(dat)
	resp=requests.post(url,json=dat)
	print(resp.json())

# def create_building():

if __name__ == "__main__":
    times = 100
    for i in range(times):
        create_user()
