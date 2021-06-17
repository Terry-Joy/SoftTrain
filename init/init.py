import requests
import random


def create_user():
    url = "http://127.0.0.1:8080/user/user_create"
    data = []
    for i in range(10):
        data.append(f'{i}')
    username = ""
    for i in range(12):
        username = username + random.choice(data)
    type = ['学生', '宿管']
    password = ""
    for i in range(15):
        password = password + random.choice(data)
    # print(username+password)
    usertype = random.choice(type)
    dat = {"user_name": username, "password": password, "user_type": usertype}
    print(dat)
    resp=requests.post(url,json=dat)
    print(resp.json())


if __name__ == "__main__":
    times = 1
    for i in range(times):
        create_user()
