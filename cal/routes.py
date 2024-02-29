from flask import Blueprint

cal = Blueprint('cal', __name__, template_folder='templates', static_folder='static',
                  static_url_path='/cal/static')


