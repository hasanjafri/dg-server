from gino import Gino

db = Gino()

from db.models import Admin
from db.models import User

async def createDb():
    async with db.with_bind('postgresql://localhost/datagramDb'):
        await db.gino.create_all()
        await User.create(fullname="Hasan Jafri")
        print(await User.query.gino.all())

if __name__ == "__main__":
    createDb()