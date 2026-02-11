from http import HTTPStatus
from typing import Annotated
from uuid import uuid4

from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .base62 import generate_short_code
from .cache import get_cached_code, set_cached_data
from .database import get_session
from .models import Url
from .schemas import UrlOut

app = FastAPI()
templates = Jinja2Templates(directory="templates")

Session = Annotated[AsyncSession, Depends(get_session)]


@app.get("/", status_code=HTTPStatus.OK)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/shorten", response_model=UrlOut, status_code=HTTPStatus.CREATED)
async def shorten(data: dict, session: Session):
    url = data.get("url")
    if not url:
        raise HTTPException(HTTPStatus.BAD_REQUEST, detail="URL é obrigatória")
    
    existing_url = await session.scalar(select(Url).where(Url.long_url == url))

    if existing_url:
        return existing_url

    short_url_object = Url(
        uuid=str(uuid4()),
        long_url=url,
        short_code=generate_short_code(),
    )

    session.add(short_url_object)
    await session.commit()
    await session.refresh(short_url_object)

    return short_url_object


@app.get("/{short_code}")
async def get_url(short_code: str, session: Session):
    cached_data = get_cached_code(short_code)

    if cached_data:
        cached_short_code = str(cached_data)
        return RedirectResponse(cached_short_code, HTTPStatus.FOUND)

    url_db = await session.scalar(select(Url).where(Url.short_code == short_code))

    if not url_db:
        raise HTTPException(HTTPStatus.NOT_FOUND, detail="URL não encontrada.")

    set_cached_data(url_db.short_code, url_db.long_url)

    return RedirectResponse(url_db.long_url, HTTPStatus.FOUND)
