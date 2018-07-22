import sys
import asyncio

from sqlalchemy import MetaData, create_engine as sa_create_engine
from aiomysql.sa import create_engine
from aiomysql.sa.engine import Engine
from config import MYSQL_CONFIG


async def init_engine():
    global engine
    engine = await create_engine(**MYSQL_CONFIG)


async def async_execute(*args, **kwargs):
    async with engine.acquire() as conn:
        return await conn.execute(*args, **kwargs)

# 新建自动识别 reflect 的 engine class，并替换掉模块中的引用
CustomEngine = type('CustomEngine', (Engine, ), dict(__getattr__=lambda _, name: meta.tables[name]))
mod = sys.modules.get('aiomysql.sa.engine')
mod.__dict__['Engine'] = CustomEngine

# 使用 sa 提供的反射机制
engine = None
mysql_conn = 'mysql://{user}:{password}@{host}:{port}/{db}?charset=utf8mb4'.format(**MYSQL_CONFIG)
_ = sa_create_engine(mysql_conn)
meta = MetaData()
meta.reflect(_)

# 初始化 engine，并为 engine 绑定具备自动连接的 excute
asyncio.get_event_loop().run_until_complete(init_engine())
engine.__dict__['execute'] = async_execute


if __name__ == '__main__':
    from sqlalchemy.sql import select
    print(type(engine))
    t = engine.tags
    print(t)
    sql = select([t])
    a = asyncio.get_event_loop().run_until_complete(engine.execute(sql))
    print(asyncio.get_event_loop().run_until_complete(a.fetchall()))