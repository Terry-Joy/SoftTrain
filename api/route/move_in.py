from fastapi import Depends,HTTPException,status
from ..typing.move_in import MoveInType
from ..depends.move_in import get_is_studentLive
from ..app import app

from typing import Optional

@app.post("/move_in/apply_for_move_in")
async def apply_for_move_in(
	apply:Optional[str]=Depends(get_is_studentLive)
):
	return {"msg":"you have applied successfully"}