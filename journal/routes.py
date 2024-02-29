from flask import Blueprint

journal = Blueprint('journal', __name__, template_folder='templates', static_folder='static',
                  static_url_path='/journal/static')