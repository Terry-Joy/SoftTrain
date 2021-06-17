# SoftTrain
homework for Software development

# 本项目配置
+ python3.8 及以上
+ pip已导入路径
+ python -m pip install -r requirement.txt
+ 参照 env_example.py 新建一个 env.py

随机64位十六进制串

```c++
openssl rand -hex 32		//只适用linux 可以去网上自己生成 or直接用我的
```





以下配置命令只适用于windows

+ env.py下更改

SECRET_KEY = "c71c7ebb7c587bb3caf03585b6ca7d0dd7b362e6e8d452581196f4e8cabd72bf"

dburl_dbs = "mysql://root:44512349875!@localhost/soft"
上面改本地数据库 用户名:密码*/数据库名

dburl_sqlalchemy = "mysql+pymysql://root:44512349875!@localhost/soft"
要改的同上

5.python -m api 运行api模块

6.此时api已经运行在 127.0.0.1:8080下



# nginx install

+ https://nginx.org/en/download.html

  [ nginx/Windows-1.21.0](https://nginx.org/download/nginx-1.21.0.zip)

+ 解压后找到nginx.conf
详见我的nginx.conf配置

		server{
				listen 8081;
				
				# ip or domain
					server_name localhost;
			
					root E:/xuexi/project/SoftTrain/SoftwareDevelopmentTraining;//前端index的路径
					index index.html;
				
					location /api/ {
						proxy_pass http://127.0.0.1:8080/;
					}
				}
	

项目运行

两个终端同时运行
项目目录下 python -m api 运行后端服务器

进入nginx安装路径下运行nginx.exe

http://localhost:8081/  主页所在

http://localhost:8081/api/****   即为后端的url

例如http://localhost:8081/api/docs 为接口文档 以后本机就按这个格式发请求即可

切记每次用完关闭前要停止所有nginx服务
nginx安装目录下  .\nginx.exe -s quit  或者 直接任务管理器全关掉(推荐)