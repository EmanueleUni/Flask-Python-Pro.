# -*- coding: utf-8 -*-
"""
Created on Sun Sep 14 12:50:58 2025

@author: Emanuele
"""

import sqlite3
from datetime import datetime

import click
from flask import current_app, g


#g non è un oggetto del database.È un oggetto speciale di Flask, chiamato “global context” per la richiesta corrente.Serve a memorizzare variabili che durano solo durante la singola richiesta.

def get_db():  #crea una connessione al db
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None): #chiude la connessione al db
    db = g.pop('db', None)

    if db is not None:
        db.close()
        
        
def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f: #apre un file nella cartella
        db.executescript(f.read().decode('utf8'))     #get_db restituisce una connessione al database, che viene utilizzata per eseguire i comandi letti dal file.


@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


sqlite3.register_converter(
    "timestamp", lambda v: datetime.fromisoformat(v.decode())
)

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    
def clear_pt():
    
    db = get_db()
    db.execute("UPDATE user SET points = 0 ")
    db.commit()
    
@click.command('clear-pt')
def clear_pt_command():
    """Clear the existing data and create new tables."""
    clear_pt()
    click.echo('clearing')
    

        
    
    