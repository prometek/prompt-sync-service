from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime

# Tables d'association many-to-many
class PromptStyleLink(SQLModel, table=True):
    prompt_id: Optional[int] = Field(default=None, foreign_key="prompt.id", primary_key=True)
    style_id: Optional[int] = Field(default=None, foreign_key="style.id", primary_key=True)

class PromptAnimalLink(SQLModel, table=True):
    prompt_id: Optional[int] = Field(default=None, foreign_key="prompt.id", primary_key=True)
    animal_id: Optional[int] = Field(default=None, foreign_key="animal.id", primary_key=True)

class PromptStatusHistory(SQLModel, table=True):
    prompt_id: Optional[int] = Field(default=None, foreign_key="prompt.id", primary_key=True)
    status_id: Optional[int] = Field(default=None, foreign_key="status.id", primary_key=True)
    changed_at: datetime = Field(default_factory=datetime.utcnow, primary_key=True)

    prompt: Optional["Prompt"] = Relationship(back_populates="history")
    status: Optional["Status"] = Relationship(back_populates="history")

# Entités principales
class Style(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)
    prompts: List["Prompt"] = Relationship(back_populates="styles", link_model=PromptStyleLink)

class Animal(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)
    prompts: List["Prompt"] = Relationship(back_populates="animals", link_model=PromptAnimalLink)

class Status(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)
    prompts: List["Prompt"] = Relationship(back_populates="status")
    history: List[PromptStatusHistory] = Relationship(back_populates="status")

class Prompt(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    prompt: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relations
    styles: List[Style] = Relationship(back_populates="prompts", link_model=PromptStyleLink)
    animals: List[Animal] = Relationship(back_populates="prompts", link_model=PromptAnimalLink)
    status_id: Optional[int] = Field(default=None, foreign_key="status.id")
    status: Optional[Status] = Relationship(back_populates="prompts")
    history: List[PromptStatusHistory] = Relationship(back_populates="prompt")

PromptStatusHistory.model_rebuild()
