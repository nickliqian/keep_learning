from sanic import Sanic
from sanic.response import text
import asyncio

app = Sanic(__name__)


@app.route("/")
@app.route("/")
async def index(req, word=""):
    t = len(word) / 10
    await asyncio.sleep(t)
    return text("It costs {}s to process `{}`!".format(t, word))


app.run()