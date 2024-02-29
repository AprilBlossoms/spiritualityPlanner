import os

from flask import Flask
from sqlalchemy import MetaData

from config import Config
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_ckeditor import CKEditor

metadata = MetaData(
    naming_convention={
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
    }
)

db = SQLAlchemy(metadata=metadata)
migrate = Migrate()
mail = Mail()
ckeditor = CKEditor()


def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    APP_ROOT = os.path.dirname(os.path.abspath(__file__))
    UPLOAD_FOLDER = os.path.join(APP_ROOT, 'static/images')
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    db.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)
    mail.init_app(app)
    ckeditor.init_app(app)

    with app.app_context():
        from spiritualityPlanner import routes, models
        from .tarot.routes import tarot
        from .cal.routes import cal
        from .astro.routes import astro
        from .journal.routes import journal
        from .sugar.routes import sugar

        app.register_blueprint(tarot)
        app.register_blueprint(cal)
        app.register_blueprint(astro)
        app.register_blueprint(journal)
        app.register_blueprint(sugar)

    return app