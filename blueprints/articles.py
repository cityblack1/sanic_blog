from sanic import Blueprint
from sanic.response import json
from app import app


articles_bp = Blueprint('articles', url_prefix='articles')


@articles_bp.route('/')
async def articles_list(request):
    return json({'articles': 'list'})


@articles_bp.route('/<article_id:int>')
async def articles_detail(request, article_id):
    return json({'articles': 'detail'})
