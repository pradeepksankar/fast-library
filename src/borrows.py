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


@router.post("/v1/borrows")
async def add_borrow(borrow: Borrow):
    await db.connection.execute(
        """
        INSERT INTO borrows
            (reader_id, book_id, borrow_time, return_time)
        VALUES
            (?, ?, DATE('now'), NULL)
        """
        if book_id not in books or reader_id not in readers:
            return jsonify({"error": "Invalid book or reader ID"}), 400

        if book.borrower_id is not None:
            if book.borrower_id != reader_id:
                return jsonify({"error": "Book is already borrowed"}), 400

        book.borrower_id = reader_id

        db.session.commit()

        return jsonify({"message": "Book borrowed"}), 200,
        (borrow.reader_id, borrow.book_id),
    )
    log.debug(f"New borrow from reader id {borrow.reader_id}")


@router.delete("/v1/borrows/{book_id}")
async def del_borrow(book_id: int):
    await db.connection.execute(
        """
        UPDATE
            borrows
        SET
            return_time = DATE('now')
        WHERE
            book_id = ?
            AND return_time IS NULL;
        """,
        (book_id,),
    )
    log.debug(f"Book {book_id} returned.")


@router.get("/v1/borrows")
async def get_borrows():
    async with db.connection.execute(
        """
        SELECT
            readers.name,
            books.title,
            authors.name,
            borrows.borrow_time
        FROM
            borrows
        LEFT JOIN
            books ON books.id = borrows.book_id
        LEFT JOIN
            authors ON authors.id = books.author_id
        LEFT JOIN
            readers ON readers.id = borrows.reader_id
        WHERE
            borrows.return_time IS NULL
        """
    ) as cursor:
        rows = await cursor.fetchall()

    return {
        "borrows": [{"reader": item[0], "title": item[1], "author": item[2], "borrow_time": item[3]} for item in rows]
    }
