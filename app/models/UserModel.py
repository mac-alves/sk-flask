from app.models.BancoDados import banco

class UserModel(banco.Model):

    __tablename__='user'

    id = banco.Column(banco.Integer, primary_key=True)
    login = banco.Column(banco.String(40), nullable=False, unique=True)
    password = banco.Column(banco.String(40), nullable=False)
    email = banco.Column(banco.String(100), nullable=False, unique=True)
    ativado = banco.Column(banco.Boolean, default=False)

    def __init__(self, login, password, email, ativado):
        self.login = login
        self.password = password
        self.email = email
        self.ativado = ativado