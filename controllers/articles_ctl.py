from models import articles as articles_dao


def format_articles():
    pass


def format_article(article):
    return dict(article)


async def get_articles(page, page_size, search=None):
    offset = (page - 1) * page_size
    limit = page_size
    articles = map(format_article, await articles_dao.get_articles(offset, limit, search=None))
    return articles


def get_article():
    pass


def create_article():
    pass
