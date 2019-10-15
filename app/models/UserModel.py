from app.models.BancoDados import banco

class UserModel(banco.Model):

    __tablename__='USER'
#alterar os campos para se adequar a api do symfony
#id
#login
#password
#email
#ativado
    ID_USER = banco.Column(banco.Integer, primary_key=True)
    LOGIN = banco.Column(banco.String(40), nullable=False, unique=True)
    PASSWORD = banco.Column(banco.String(40), nullable=False)
    EMAIL = banco.Column(banco.String(100), nullable=False, unique=True)
    ATIVADO = banco.Column(banco.Boolean, default=False)

    def __init__(self, login, password, email, ativado):
        self.LOGIN = login
        self.PASSWORD = password
        self.EMAIL = email
        self.ATIVADO = ativado