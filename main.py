from quart import Quart, render_template, websocket
from books.book import MyBookSource

app = Quart(__name__)


@app.route("/")
async def hello():
    return await render_template("ws.html")


@app.route("/api")
async def json():
    return {"hello": "world"}


@app.websocket("/ws")
async def ws():
    while True:
        data = await websocket.receive()
        MyBookSource.search_by_title(data)
        books = {"books": MyBookSource.books}
        #  await websocket.send(f"hello {data}")
        await websocket.send_json(books)
        #  await websocket.send_json({"books": [
        #      ('Пикник на обочине', 'https://asdf.com/'),
        #      ('Преступление и наказание', 'https://sfajfjfjff.com/'),
        #  ]})

if __name__ == "__main__":
    app.run()
