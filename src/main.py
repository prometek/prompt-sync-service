from contextlib import asynccontextmanager

from fastapi import FastAPI, Response, Depends, HTTPException
from pydantic_settings import BaseSettings
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select, SQLModel



from src.database import  get_session, async_engine
from src.models import Prompt, Style, Animal, Status, PromptStatusHistory


class Settings(BaseSettings):
    host: str = "0.0.0.0"
    port: int = 8000


settings = Settings()
app = FastAPI()

REQUEST_COUNT = Counter("request_count", "Total HTTP requests")

@asynccontextmanager
async def lifespan():
    # for an async engine you need to run create_all via run_sync:
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    yield


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/metrics")
async def metrics():
    data = generate_latest()
    return Response(content=data, media_type=CONTENT_TYPE_LATEST)


@app.get("/")
async def root():
    REQUEST_COUNT.inc()
    return {"message": "Hello from {{ service_name }}"}

# Endpoint pour ajouter ou récupérer un style
@app.post("/styles/{name}")
async def create_style(name: str, session: AsyncSession = Depends(get_session)):
    statement = select(Style).where(Style.name == name)
    result = await session.exec(statement)
    style = result.one_or_none()
    if style:
        return style
    style = Style(name=name)
    session.add(style)
    await session.commit()
    await session.refresh(style)
    return style

@app.get("/styles")
async def read_styles(session: AsyncSession = Depends(get_session)):
    result = await session.exec(select(Style))
    return result.all()

# Endpoint pour ajouter ou récupérer un animal
@app.post("/animals/{name}")
async def create_animal(name: str, session: AsyncSession = Depends(get_session)):
    statement = select(Animal).where(Animal.name == name)
    result = await session.exec(statement)
    animal = result.one_or_none()
    if animal:
        return animal
    animal = Animal(name=name)
    session.add(animal)
    await session.commit()
    await session.refresh(animal)
    return animal

@app.get("/animals")
async def read_animals(session: AsyncSession = Depends(get_session)):
    result = await session.exec(select(Animal))
    return result.all()

# Endpoint pour créer un status
@app.post("/statuses/{name}")
async def create_status(name: str, session: AsyncSession = Depends(get_session)):
    statement = select(Status).where(Status.name == name)
    result = await session.exec(statement)
    status = result.one_or_none()
    if status:
        return status
    status = Status(name=name)
    session.add(status)
    await session.commit()
    await session.refresh(status)
    return status

@app.get("/statuses")
async def read_statuses(session: AsyncSession = Depends(get_session)):
    result = await session.exec(select(Status))
    return result.all()

# Endpoint pour créer un prompt avec associations
@app.post("/prompts/")
async def create_prompt(
    prompt: str,
    styles: list[str],
    animals: list[str],
    status: str,
    session: AsyncSession = Depends(get_session)
):
    # Création ou récupération du status
    stmt_status = select(Status).where(Status.name == status)
    status_obj = (await session.exec(stmt_status)).one_or_none()
    if not status_obj:
        status_obj = Status(name=status)
        session.add(status_obj)
        await session.commit()
        await session.refresh(status_obj)
    # Création ou récupération des styles
    style_objs = []
    for s in styles:
        stmt = select(Style).where(Style.name == s)
        obj = (await session.exec(stmt)).one_or_none()
        if not obj:
            obj = Style(name=s)
            session.add(obj)
            await session.commit()
            await session.refresh(obj)
        style_objs.append(obj)
    # Création ou récupération des animals
    animal_objs = []
    for a in animals:
        stmt = select(Animal).where(Animal.name == a)
        obj = (await session.exec(stmt)).one_or_none()
        if not obj:
            obj = Animal(name=a)
            session.add(obj)
            await session.commit()
            await session.refresh(obj)
        animal_objs.append(obj)
    # Création du prompt
    new_prompt = Prompt(prompt=prompt, status_id=status_obj.id)
    session.add(new_prompt)
    await session.commit()
    await session.refresh(new_prompt)
    # Associations
    new_prompt.styles = style_objs
    new_prompt.animals = animal_objs
    session.add(new_prompt)
    await session.commit()
    await session.refresh(new_prompt)
    # Ajout historique
    history = PromptStatusHistory(prompt_id=new_prompt.id, status_id=status_obj.id)
    session.add(history)
    await session.commit()
    await session.refresh(history)
    return new_prompt


@app.get("/prompts")
async def read_prompts(session: AsyncSession = Depends(get_session)):
    result = await session.exec(select(Prompt))
    return result.all()

@app.get("/prompts/{prompt_id}")
async def read_prompt(prompt_id: int, session: AsyncSession = Depends(get_session)):
    result = await session.exec(select(Prompt).where(Prompt.id == prompt_id))
    prompt = result.one_or_none()
    if not prompt:
        raise HTTPException(status_code=404, detail="Prompt not found")
    return prompt
