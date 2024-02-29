from flask import Blueprint

tarot = Blueprint('tarot', __name__, template_folder='templates', static_folder='static',
                  static_url_path='/tarot/static')