from flask import Flask, jsonify
from config import config
from app.models.BancoDados import banco
from flask_jwt_extended import JWTManager
from config import DevelopmentConfig, BLACKLIST

from .api import configure_api

def create_app(config_name):
    app = Flask(__name__)

    app.config.from_object(config[config_name])

    jwt = JWTManager(app)

    @app.before_first_request
    def cria_banco():
        banco.create_all()

    @jwt.token_in_blacklist_loader
    def verificar_blacklist(token):
        return token['jti'] in BLACKLIST

    @jwt.revoked_token_loader
    def token_de_acesso_invalidado():
        return jsonify({'msg':'You have been logged out.'}), 401

    # executa a chamada da função de configuração
    configure_api(app)

    return app