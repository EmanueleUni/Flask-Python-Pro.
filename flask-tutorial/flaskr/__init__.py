# -*- coding: utf-8 -*-
"""
Created on Sun Sep 14 11:55:58 2025

@author: Emanuele
"""

import os 

from flask import Flask


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    from .db import init_app  #importo la funzione init_app() che chiama init_db() che inizializa il db
    init_app(app)

    from . import auth        #registro il bp creato con auth
    app.register_blueprint(auth.bp)
    
    from .weather import bp as weather_bp
    app.register_blueprint(weather_bp, url_prefix='/weather')
    
    from . import quiz
    app.register_blueprint(quiz.bp)
    
    from .db import clear_pt_command  # importa il comando
    app.cli.add_command(clear_pt_command)   
    
    
    return app


