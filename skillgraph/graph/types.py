from uuid import uuid4

from pydantic import BaseModel, Field


class Skill(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    name: str
    description: str
    proficiency: float = Field(default=0.0, ge=0.0, le=1.0)

