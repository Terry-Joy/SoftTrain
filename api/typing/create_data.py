import random
from typing import Optional


def first_name():  #   随机取姓氏字典
    first_name_list = [
        '赵', '钱', '孙', '李', '周', '吴', '郑', '王', '冯', '陈', '褚', '卫', '蒋', '沈', '韩', '杨', '朱', '秦', '尤', '许',
        '何', '吕', '施', '张', '孔', '曹', '严', '华', '金', '魏', '陶', '姜', '戚', '谢', '邹', '喻', '柏', '水', '窦', '章',
        '云', '苏', '潘', '葛', '奚', '范', '彭', '郎', '鲁', '韦', '昌', '马', '苗', '凤', '花', '方', '俞', '任', '袁', '柳',
        '酆', '鲍', '史', '唐', '费', '廉', '岑', '薛', '雷', '贺', '倪', '汤', '滕', '殷', '罗', '毕', '郝', '邬', '安', '常',
        '乐', '于', '时', '傅', '皮', '卞', '齐', '康', '伍', '余', '元', '卜', '顾', '孟', '平', '黄', '和', '穆', '萧', '尹',
        '姚', '邵', '堪', '汪', '祁', '毛', '禹', '狄', '米', '贝', '明', '臧', '计', '伏', '成', '戴', '谈', '宋', '茅', '庞',
        '熊', '纪', '舒', '屈', '项', '祝', '董', '梁','国','郭','高','姚','庄','林','杜','欧阳','诸葛','慕容','独孤']
    n = random.randint(0, len(first_name_list) - 1)
    f_name = first_name_list[n]
    return f_name

def last_name():
	last_name_list=[
		'天', '乐', '国', '良', '焜', '茗', '红', '伟', '倩', '越', '家', '文', '杰', '强', '云', '舒', '春', '阳', '浩', '民',
        '珊', '婷', '元', '俊', '峰', '昱', '德', '云', '飞', '扬', '斯', '超', '彦', '浩', '腾', '梦', '月', '秀', '多', '迪',
        '军', '庆', '耀', '青', '昌', '熔', '希', '郎', '津', '泽', '瑜', '羽', '嘉', '佳', '灵', '丹', '登', '敏', '君', '宏',
        '构', '洪', '兵', '斌', '武', '文', '玮', '胜', '奖', '舟', '洲', '州', '子', '方', '芳', '二', '行', '一', '化', '东',
        '爷', '若', '晴', '阴', '雄', '诗', '宇', '辰', '涵', '健', '君', '智', '慧', '惠', '珲', '晖', '辉', '金', '鸿', '玉',
        '薇', '雪', '捷', '昊', '洁', '达', '开', '航', '凯', '贝', '明', '娴', '帆', '非', '凡', '暄', '盈', '华', '运', '婷',
		'雨', '逸', '民', '名', '聪', '尽', '玠', '卓'
	]
	l_name=''.join(random.sample(last_name_list,random.randint(1,2)))
	return l_name


def create_school():
	school=['机械与汽车工程学院','建筑学院','土木与交通学院','电子与信息学院','材料科学与工程学院','化学与化工学院','轻工科学与工程学院','食品科学与工程学院','数学学院',
	'物理与光电学院','经济与贸易学院','自动化科学与工程学院','计算机科学与工程学院','电力学院','生物科学与工程学院','环境与能源学院','软件学院','工商管理学院','公共管理学院','外国语学院','法学院',
	'新闻与传播学院','艺术学院','体育学院','设计学院','医学院']
	str=random.choice(school)
	return str


def create_name():
	return first_name()+last_name()


def create_sex()->str:
	a=random.randint(0,1)
	if(a==0):
		return "male"
	else:
		return "females"


def create_grade()->int:
	a=random.randint(2019,2023)
	return a


def create_now_class():
	a=random.randint(1,6)
	return a


def create_live_status()->str:
	a=random.randint(0,1)
	if(a==0):
		return "yes"
	else:
		return "no"


def create_phone_number()->str:
	phone_sta=['133','131','132','133','138','134','135','136','137','171','175','139','155','173','177','175','176','185']
	phone_start=random.choice(phone_sta)
	str_end=''.join(random.sample('0123456789',8))
	str_phone=phone_start+str_end
	return str_phone


def create_bel_b_name(flag:int,sex:Optional[str]=None,bel_school:Optional[str]=None)->str:
	pos=[]
	mp=[]
	for i in range(1,53):
		pos.append(f'{i}')
	for i in range(len(pos)):
		pos[i]='C'+pos[i]
	for i in range(0,51,2):
		mp.append(i)
	school=['机械与汽车工程学院','建筑学院','土木与交通学院','电子与信息学院','材料科学与工程学院','化学与化工学院','轻工科学与工程学院','食品科学与工程学院','数学学院',
	'物理与光电学院','经济与贸易学院','自动化科学与工程学院','计算机科学与工程学院','电力学院','生物科学与工程学院','环境与能源学院','软件学院','工商管理学院','公共管理学院','外国语学院','法学院',
	'新闻与传播学院','艺术学院','体育学院','设计学院','医学院']
	mydict=dict(zip(school,mp))
	pos.append('all')
	if flag==0:
		str=random.choice(pos)
		return str
	else:
		base=mydict[bel_school]
		if sex=='male':
			return pos[base] 
		else:
			return pos[base+1] 


def create_building(building:int):
	sex=""
	if building%2==0:
		sex="female"
	else:
		sex="male"
	school=['机械与汽车工程学院','建筑学院','土木与交通学院','电子与信息学院','材料科学与工程学院','化学与化工学院','轻工科学与工程学院','食品科学与工程学院','数学学院',
	'物理与光电学院','经济与贸易学院','自动化科学与工程学院','计算机科学与工程学院','电力学院','生物科学与工程学院','环境与能源学院','软件学院','工商管理学院','公共管理学院','外国语学院','法学院',
	'新闻与传播学院','艺术学院','体育学院','设计学院','医学院']
	str='C'+f"{building}"
	a=(int)(building/2)
	return {"building_id":str,"sex":sex,"school":school[a]}


def create_bel_d_number()->str:
	pos=[]
	for i in range(1,60):
		pos.append(f'{i}')
	for i in range(len(pos)):
		if(len(pos[i])<=1):
			pos[i]='0'+pos[i]
	first=''.join(random.sample('1234567',1))
	return first+random.choice(pos)


def create_id(num:int=12)->str:
	data=[]
	for i in range(10):
		data.append(f'{i}')	
	id = ""
	for i in range(num):
		id = id + random.choice(data)
	return id

