from pydantic import BaseModel, Field
from typing import Optional

class Vacancy(BaseModel):
    id: str
    name: str
    area_name: str
    salary_from: Optional[int] = None
    salary_to: Optional[int] = None
    experience: Optional[str] = None 
    requirement: Optional[str] = None 
    responsibility: Optional[str] = None 
    alternate_url: str