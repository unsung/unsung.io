import logging
logger = logging.getLogger(__name__)

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

from flask_bootstrap import Bootstrap, WebCDN
Bootstrap(app)
app.extensions['bootstrap']['cdns']['bootstrap'] = WebCDN(
    'https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/'
)
app.extensions['bootstrap']['cdns']['jquery'] = WebCDN(
    'https://cdnjs.cloudflare.com/ajax/libs/jquery/3.1.1/'
)

from . import config
app.config.from_object(config.DefaultConfig)

import os
CONFIG_ENVVAR = 'UNSUNGIO_CONFIG'
config_env = os.getenv(CONFIG_ENVVAR)
if config_env is not None:
    try:
        config.from_pyfile(config_env)
    except Exception:
        logging.exception('%s is not set correctly' % CONFIG_ENVVAR)


db = SQLAlchemy(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

#from app.mod_auth.controllers import mod_auth as auth_module
#app.register_blueprint(auth_module)

db.create_all()
