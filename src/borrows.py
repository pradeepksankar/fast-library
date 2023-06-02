import logging
from datetime import datetime
from typing import Optional

from fastapi import APIRouter
from pydantic import BaseModel

from . import db


log = logging.getLogger(__name__)
router = APIRouter()


class Borrow(BaseModel):
    reader_id: int
    book_id: int
    borrow_time: datetime
    return_time: Optional[datetime] = None


@router.post("/v1/borrows")
async def add_borrow(borrow: Borrow):
    await db.connection.execute(
        """
        INSERT INTO borrows
            (reader_id, book_id, borrow_time, return_time)
        VALUES (?, ?, ?, ?)
        """,
        (borrow.reader_id, borrow.book_id, borrow.borrow_time, borrow.return_time),
    )

    log.debug(f"New borrow from reader id {borrow.reader_id}")


@router.get("/v1/borrows/{reader_id}")
async def get_borrows(reader_id: int):
    async with db.connection.execute(
        """
        SELECT
            borrows.id,
            books.title,
            authors.name,
            borrows.borrow_time
        FROM
            borrows
        JOIN
            books ON books.id = borrows.book_id
        JOIN
            authors ON authors.id = books.author_id
        WHERE
            borrows.return_time IS NULL
        """
    ) as cursor:
        rows = await cursor.fetchall()

    return {"borrows": [{"id": item[0], "title": item[1], "author": item[2], "borrow_time": item[3]} for item in rows]}
