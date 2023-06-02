import asyncio
from fastapi import FastAPI
from uvicorn import Config, Server

from .db import db

from . import books
from . import authors

app = FastAPI()

app.include_router(books.router)
app.include_router(authors.router)


@app.get("/")
async def root():
    return 'Book Library'


@app.on_event("shutdown")
async def app_shutdown():
    await db.connection.close()
    asyncio.get_event_loop().stop()


if __name__ == "__main__":

    web_server = Server(
        Config(app=app, host='0.0.0.0', port=8000)
    )
    loop = asyncio.get_event_loop()
    loop.call_soon(lambda: asyncio.create_task(db.init_db()))
    loop.call_soon(lambda: asyncio.create_task(web_server.serve()))
    loop.run_forever()
