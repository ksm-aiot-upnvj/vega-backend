from typing import Optional
from pydantic import BaseModel

class CategoryBase(BaseModel):
    name: str
    slug: str
    description: Optional[str] = None

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(CategoryBase):
    name: Optional[str] = None
    slug: Optional[str] = None

class CategoryInDBBase(CategoryBase):
    id: str
    course_count: Optional[int] = 0

    class Config:
        from_attributes = True

class Category(CategoryInDBBase):
    pass
