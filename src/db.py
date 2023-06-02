import logging
import os

import aiosqlite


log = logging.getLogger(__name__)


class Database:
    def __init__(self):
        self.connection = None

    async def init_db(self):
        log.debug(f"Initializing db")

        self.connection = await aiosqlite.connect(f"{os.getcwd()}/db.sqlite")

        await self.connection.execute(
            """
            CREATE TABLE IF NOT EXISTS authors (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL
            )
            """
        )

        await self.connection.execute(
            """
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY,
                author_id INTEGER NOT NULL,
                title TEXT NOT NULL
            )
            """
        )

        await self.connection.execute(
            """
            CREATE TABLE IF NOT EXISTS readers (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL
            )
            """
        )

        await self.connection.execute(
            """
            CREATE TABLE IF NOT EXISTS borrows (
                id INTEGER PRIMARY KEY,
                reader_id INTEGER NOT NULL,
                book_id INTEGER NOT NULL,
                borrow_time TEXT NOT NULL,
                return_time TEXT
            )
            """
        )


db = Database()
