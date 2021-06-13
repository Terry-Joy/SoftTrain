from __future__ import annotations

from datetime import datetime,timedelta

from jose import jwt 
from ..env import SECRET_KEY
from pydantic import BaseModel
from typing import Optional
from .user import UserInDB

class Token(BaseModel):
	access_token:str
	token_type:str

class jwtToken(BaseModel):
	#user_id
	sub:str 
	#end
	exp:datetime
	#start
	iat:datetime

	def encode(self)->str:
		return jwt.encode(
			self.dict(),
			SECRET_KEY,
			algorithm='HS256'
		)
	
	@classmethod
	def get_newjwt(cls,user:UserInDB)->str:
		now_time=datetime.utcnow()
		obj=cls(
			sub=user.uid,
			exp=now_time+timedelta(minutes=30),
			iat=now_time
		)
		return obj.encode()

	@staticmethod
	def decode(token:Optional[str])->Optional[jwtToken]:
		if not token:
			return None
		return jwtToken.parse_obj(
			jwt.decode(
				token,
				SECRET_KEY,
				algorithm=['HS256'],
			)
		)