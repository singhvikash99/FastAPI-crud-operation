from pydantic import BaseModel
from fastapi import Query
from typing import Optional


class NewStudent(BaseModel):
    name:str
    std:int = Query(le=12, ge=1)
    roll_number:int

class NewSubject(BaseModel):
    subject:str

class UpdateStudent(BaseModel):
    name:Optional[str] = None
    std:Optional[int] = Query(le=12, ge=1, default= None)
    roll_number:Optional[int] = None