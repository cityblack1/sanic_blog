from sanic import Blueprint
from sanic.response import json

from controllers import articles_ctl

articles_bp = Blueprint('articles', url_prefix='articles')


@articles_bp.route('/')
async def articles_list(request):
    page = request.args.get('page', 1)
    page_size = request.args.get('pageSize', 5)
    search = request.args.get('search', None)
    articles = await articles_ctl.get_articles(page, page_size, search)
    return json({'articles': articles})


@articles_bp.route('/<article_id:int>')
async def articles_detail(request, article_id):
    return json({'articles': 'detail'})
