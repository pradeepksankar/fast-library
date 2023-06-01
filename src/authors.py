from fastapi import APIRouter, Response, status
from pydantic import BaseModel

from .db import db
from .log import log


router = APIRouter()


class Author(BaseModel):
    name: str


@router.post('/v1/authors')
async def add_author(author: Author):

    await db.connection.execute('''
        INSERT INTO authors
        VALUES (?, ?)
        ''', (None, author.name))
    log.debug(f'Author added {author.name}')


@router.get('/v1/authors')
async def get_authors():

    async with db.connection.execute('''
        SELECT
            id, name
        FROM
            authors
        ORDER BY id ASC
        ''') as cursor:
        rows = await cursor.fetchall()

    return {
        "authors": [{
            "id": item[0], "name": item[1]
        } for item in rows]
    }
