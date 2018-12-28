import sys
sys.path.append('../')

import asyncio
from gino import Gino

db = Gino()

from db.models import Admin
from db.models import User

async def createDb():
    await db.set_bind('postgresql://postgres:admin3@localhost:5432/datagramDb')
    await db.gino.create_all()
    await User.create(fullname="Hasan Jafri")
    print(await User.query.gino.all())

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(createDb())