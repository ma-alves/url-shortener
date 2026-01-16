from http import HTTPStatus

from fastapi import FastAPI
from hashids import Hashids

from settings import Settings
from schemas import Message


app = FastAPI()


@app.get("/", response_model=Message, status_code=HTTPStatus.OK)
async def index():
    return {"message": "OK"}


@app.post("/shorten", status_code=HTTPStatus.CREATED)
async def shorten_url(url: str):
    encoded_url = Hashids(
        salt=Settings().SECRET_KEY,  # type: ignore
        alphabet="0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ",
    )
    return encoded_url  # return json url object


@app.get("/<short-code>", status_code=HTTPStatus.MOVED_PERMANENTLY)
async def redirect_url(): ...
