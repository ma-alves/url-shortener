from contextlib import asynccontextmanager
from http import HTTPStatus
from typing import Annotated

from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import HttpUrl
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from base62 import generate_short_code
from database import get_session, sessionmanager
from models import Url
from schemas import Message, UrlOut


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    if sessionmanager._engine is not None:
        await sessionmanager.close()


app = FastAPI(lifespan=lifespan)

Session = Annotated[AsyncSession, Depends(get_session)]


@app.get("/", response_model=Message, status_code=HTTPStatus.OK)
async def index():
    return {"message": "http://127.0.0.1:8000/docs#/"}


@app.post("/shorten", response_model=UrlOut, status_code=HTTPStatus.CREATED)
async def shorten(url: HttpUrl, session: Session):
    existing_url = await session.scalar(select(Url).where(Url.long_url == str(url)))
    
    if existing_url:
        return existing_url

    short_url_object = Url(
        short_code=generate_short_code(),
        long_url=str(url),
    )

    session.add(short_url_object)
    await session.commit()
    await session.refresh(short_url_object)

    return short_url_object


@app.get("/{short_code}", status_code=HTTPStatus.MOVED_PERMANENTLY)
async def get_url(short_code: str, session: Session):
    url_db = await session.scalar(select(Url).where(Url.short_code == short_code))

    if not url_db:
        raise HTTPException(HTTPStatus.NOT_FOUND, detail='URL não encontrada.')

    return RedirectResponse(url_db.long_url, HTTPStatus.MOVED_PERMANENTLY)
