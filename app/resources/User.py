from flask_restful import reqparse
from flask import make_response, render_template, Blueprint
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import create_access_token, jwt_required, get_raw_jwt
from app.controllers.UserController import UserController
from config import BLACKLIST
import traceback
import os

atributos = reqparse.RequestParser()
atributos.add_argument('login', type=str)
atributos.add_argument('password', type=str, required=True, help="The field 'password' cannot be left blank")
atributos.add_argument('ativado', type=bool)
atributos.add_argument('email', type=str, )

bp = Blueprint('user', __name__)

@bp.route('/user/<int:id_user>', methods=('GET',))
@jwt_required
def ViewUser(id_user):
    
    user = UserController.find_user(id_user)

    if user:
        return user.json()

    return {'msg':'User Not Found'}, 404 #not found


@bp.route('/user/<int:id_user>', methods=('PUT',))
@jwt_required
def UpdateUser(id_user):
    dados = atributos.parse_args()
        
    user = UserController.find_user(id_user)

    if user:
        user.update_user(dados.get('password'))
        try:
            user.save_user()
            #desloga o usuario
            jwt_id = get_raw_jwt()['jti'] #JWT token Identifier
            BLACKLIST.add(jwt_id)
        except:
            traceback.print_exc()
            return {'msg':'An internal error ocurred trying to update hotel.'}, 500

        return {'msg':'Password successfully modified. Log in again!'}, 200 #ok 

    return {'msg':'User not found.'}, 404 #Internal server error
    
    
@bp.route('/user/<int:id_user>', methods=('DELETE',))
@jwt_required
def DeleteUser(id_user):
    user = UserController.find_user(id_user)

    if user:
        try:
            user.delete_user()
        except:
            traceback.print_exc()
            return {'msg': 'An error ocurred trying to delete user'}, 500

        return {'msg':'User Deleted'}

    return {'msg':'User Not Found'}, 404


@bp.route('/register', methods=('POST',))
def UserRegister():
    
    dados = atributos.parse_args()
    
    if not dados.get('email') or dados.get('email') is None:
        return {"msg":"The field 'email' cannot be left black"}, 400

    if UserController.find_by_email(dados.get('email')):
        return {"msg":"The email '{}' already exists".format(dados.get('email'))}, 400

    if (not dados.get('login')) or (dados.get('login') is None):
        return {"msg": "The field 'login' cannot be left blank"}
        
    if UserController.find_by_login(dados['login']):
        return {"msg":"The login '{}' already exists".format(dados['login'])}
        
    user = UserController(**dados)
    user.ativado = False

    try:
        user.save_user()
        user.send_confirmation_email()
    except:
        user.delete_user()
        traceback.print_exc()
        return {'msg':'An internal server error has ocurred'}, 500

    return {'msg':'User created successfully!'}, 201 # created


@bp.route('/confirm/<int:id_user>', methods=('GET',))
def UserConfirm(id_user):
    user = UserController.find_user(id_user)

    if not user:
        return {"msg":"User id '{}' not found".format(id_user)}, 404

    user.ativado = True
    user.save_user()

    #return {"msg":"User id '{}' confirmed successfully".format(user_id)}, 200    
    headers = {'Content-Type':'text/html'}
    return make_response(render_template('user_confirm.html', email=user.email, usuario=user.login), 200, headers)


@bp.route('/login', methods=('POST',))
def UserLogin():
    dados = atributos.parse_args()

    user = UserController.find_by_login(dados['login'])

    if user and safe_str_cmp(user.password, dados['password']):
        if user.ativado:
            token_de_acesso = create_access_token(identity=user.id)
            return {'access_token':token_de_acesso}, 200
            
        return {'msg': 'User not confirmed'}, 400

    return {'msg':'The username or password is incorrect.'}, 401 #não autorizado


@bp.route('/logout', methods=('POST',))
@jwt_required
def UserLogout():
    jwt_id = get_raw_jwt()['jti'] #JWT token Identifier
    BLACKLIST.add(jwt_id)
    return {'msg':'Logged out successfully!'}, 200