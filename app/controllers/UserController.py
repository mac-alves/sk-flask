from app.models.UserModel import UserModel
from app.models.BancoDados import banco
from flask import request, url_for
from os import getenv
from requests import post

class UserController(UserModel):

    def send_confirmation_email(self):
        #'http://0.0.0.0:5000/confirm/{id_user}'
        link  = request.url_root[:-1] + url_for('user.UserConfirm', id_user=self.id)

        return post('https://api.mailgun.net/v3/{}/messages'.format(getenv('MAILGUN_DOMAIN')),
                    auth=('api', getenv('MAILGUN_API_KEY')),
                    data={'from':'{} <{}>'.format(getenv('FROM_TITLE'), getenv('FROM_EMAIL')),
                          'to': self.email,
                          'subject':'Confirmação de Cadastro',
                          'text':'Confirme seu cadastro clicando no link a seguir: {}'.format(link),
                          'html':'<html><p>\
                              Confirme seu cadastro clicando no link a seguir: <a href={}> CONFIRMAR EMAIL </a>\
                                  </p></html>'.format(link)
                          }
                    )
    
    def json(self):
        return {
            'id_user': self.id,
            'login':self.login,
            'email':self.email,
            'ativado':self.ativado
        }
    
    @classmethod
    def find_user(cls, user_id):
        user = cls.query.filter_by(id=user_id).first() #SELECT * FROM usuarios WHERE user_id=user_id LIMIT 1
        if user:
            return user
        return None

    @classmethod
    def find_by_login(cls, login):
        user = cls.query.filter_by(login=login).first() #SELECT * FROM usuarios WHERE user_id=user_id LIMIT 1
        if user:
            return user
        return None

    @classmethod
    def find_by_email(cls, email):
        email = cls.query.filter_by(email=email).first() 
        if email:
            return email
        return None

    def update_user(self, password):
        self.password = password
    
    def save_user(self):
        banco.session.add(self)
        banco.session.commit()

    def delete_user(self):
        banco.session.delete(self)
        banco.session.commit()

