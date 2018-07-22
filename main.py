from app import app
from blueprints import articles_bp


app.blueprint(articles_bp)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='9000')
