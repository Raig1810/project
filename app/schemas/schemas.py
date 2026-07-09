from pydantic import BaseModel, Field
from typing import Optional

class StudentCreate(BaseModel):
    name: str = Field(..., min_length=1, description="Имя студента")
    group: str = Field(..., min_length=1, description="Группа")
    average_score: float = Field(..., ge=0, le=100, description="Средний балл")
    
class StudentUpdate(BaseModel):
    new_name: Optional[str] = Field(None, min_length=1)
    new_score: Optional[float] = Field(None, ge=0, le=100)