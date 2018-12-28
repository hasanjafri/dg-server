from asyncio import get_event_loop
from gino import Gino

db = Gino()

async def createDb():
    await db.set_bind()
    await db.gino.create_all()

    await db.pop_bind().close()

if __name__ == "__main__":
    get_event_loop().run_until_complete(createDb())