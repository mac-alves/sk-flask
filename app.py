from os import getenv
from os.path import dirname, isfile, join

from dotenv import load_dotenv

_ENV_FILE = join(dirname(__file__), '.env')

if isfile(_ENV_FILE):
    load_dotenv(dotenv_path=_ENV_FILE)

from app import create_app

app = create_app(getenv('FLASK_ENV') or 'default')

if __name__ == '__main__':
    from app.models.BancoDados import banco

    ip = '0.0.0.0'
    port = app.config['APP_PORT']
    debug = app.config['DEBUG']
    
    banco.init_app(app)
    
    # executa o servidor web do flask
    app.run(
        host=ip, debug=debug, port=port, use_reloader=debug
    )