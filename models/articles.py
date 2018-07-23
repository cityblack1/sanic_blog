from sqlalchemy import select, and_, or_, desc
from database.mysql import db


async def get_articles(offset, limit, search=None):
    t = db.articles
    sql = select([t])
    sql = sql.offset(offset).limit(limit)
    sql = sql.order_by(t.c.id.desc())
    res = await db.execute(sql)
    return await res.fetchall()

