from quart import Quart, render_template, websocket

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
        await websocket.send(f"hello {data}")
        await websocket.send_json({"hello": data})

if __name__ == "__main__":
    app.run()
