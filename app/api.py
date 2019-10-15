from flask import Blueprint
from flask_restful import Api 

bp_home = Blueprint('home', __name__)

@bp_home.route('/', methods=('GET',))
def Index():
    return {'Home': 'Home'}

api = Api()

def configure_api(app):

    from app.resources.User import bp as bp_user

    app.register_blueprint(bp_home)
    app.register_blueprint(bp_user)

    api.init_app(app)