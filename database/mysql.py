import sys
import asyncio

from sqlalchemy import MetaData, create_engine as sa_create_engine
from aiomysql.sa import create_engine
from aiomysql.sa.engine import Engine
from config import MYSQL_CONFIG


async def async_execute(*args, **kwargs):
    async with real_engine.acquire() as conn:
        return await conn.execute(*args, **kwargs)


async def proxy_engine_init(self, *args, **kwargs):
    global real_engine
    loop = asyncio.get_event_loop()
    real_engine = await create_engine(**MYSQL_CONFIG, loop=loop)
    self.__dict__['execute'] = async_execute
    return await async_execute(*args, **kwargs)


real_engine = None
# 新建自动识别 reflect 的 engine class，并替换掉模块中的引用
CustomEngine = type('CustomEngine', (Engine, ), dict(__getattr__=lambda _, name: meta.tables[name]))
mod = sys.modules.get('aiomysql.sa.engine')
mod.__dict__['Engine'] = CustomEngine

# 使用 sa 提供的反射机制
mysql_conn = 'mysql://{user}:{password}@{host}:{port}/{db}?charset=utf8mb4'.format(**MYSQL_CONFIG)
_ = sa_create_engine(mysql_conn)
meta = MetaData()
meta.reflect(_)

ProxyEngine = type('ProxyEngine', (object, ), dict(execute=proxy_engine_init,
                                                   __getattr__=lambda _, name: meta.tables[name]))
db = engine = ProxyEngine()
