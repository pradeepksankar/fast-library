from fastapi import APIRouter, Response, status
from pydantic import BaseModel

from .db import db
from .log import log


router = APIRouter()


class Reader(BaseModel):
    name: str


@router.post('/v1/readers')
async def add_reader(reader: Reader):

    await db.connection.execute('''
        INSERT INTO readers
            (name)
        VALUES (?)
        ''', (reader.name))
    log.debug(f'Reader added {reader.name}')


@router.get('/v1/readers')
async def get_readers():

    async with db.connection.execute('''
        SELECT
            id,
            name
        FROM
            readers
        ''') as cursor:
        rows = await cursor.fetchall()

    return {
        "readers": [{
            "id": item[0],
            "name": item[1]
        } for item in rows]
    }
