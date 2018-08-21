import logging
import os
import sys
from pathlib import Path

from flask import Flask, render_template

from db.models import db
from db.setup import load_db
from rest.views import city_blueprints


PROJECT_ROOT_PATH = Path().resolve()

CITIES_TXT_FILE_LOCATION = os.path.join(PROJECT_ROOT_PATH, 'db', 'resources', 'cities1000.txt')

DB_URI = 'sqlite:////{}/test.db'.format(PROJECT_ROOT_PATH)


def register_blueprints(app_):
    app_.register_blueprint(city_blueprints, url_prefix='/city')


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
    register_blueprints(app)
    return app


app = create_app()

logger = logging.basicConfig(stream=sys.stdout, level=logging.INFO)


@app.route('/')
def index():
    # return 'Welcome!'
    return render_template('index.html')


if __name__ == "__main__":
    db.init_app(app)
    app.run()


