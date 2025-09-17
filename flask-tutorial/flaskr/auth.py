# -*- coding: utf-8 -*-
"""
Created on Sun Sep 14 11:55:58 2025

@author: Emanuele
"""

import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')




@bp.route('/register', methods=('GET', 'POST'))    #la rotta sarà /auth/register
def register():
    if request.method == 'POST':   #se l'utente invia il form html (request.method == 'POST') si procede con la validazione
        
        print(request.form)
    
        username = request.form['username']  #request.form() è un dizionario (un ImmutableMultiDict) che contiene tutti i dati inviati da un form HTML tramite POST
        password = request.form['password']
        confpass = request.form['confpassword']
        db = get_db()
        error = None

        #Validate that username and password are not empty.
        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif not confpass:
            error = 'Confirm Password is required.'
        elif password != confpass:
            error= 'the passwords entered do not match'
            
        #If validation succeeds, insert the new user data into the database.
        if error is None:
            try:
                db.execute(
                    "INSERT INTO user (username, password) VALUES (?, ?)",
                    (username, generate_password_hash(password)),
                ) #db.execute() accetta una query SQL con segnaposto ? per qualsiasi input utente e una tupla di valori con cui sostituire i segnaposto.
               
                db.commit()  #necessario richiamare db.commit() in seguito per salvare le modifiche di generate_password_hash()
           
            except db.IntegrityError:
                error = f"User {username} is already registered."
            else:
                return redirect(url_for("auth.login"))  #Dopo aver memorizzato l'utente, questo viene reindirizzato alla pagina di login. url_for() genera l'URL per la vista di login in base al suo nome. 
                #In Flask, url_for("auth.login") non è una stringa di URL, ma un modo per generare dinamicamente l’URL di una view a partire dal nome della funzione che la gestisce per questo non è /auth/login
        
        flash(error)  #flash() memorizza i messaggi che possono essere recuperati durante il rendering del modello. 

    return render_template('auth/register.html') #render_template() visualizzerà un modello contenente l'HTML salvato in 'register.html'.




@bp.route('/login', methods=('GET', 'POST')) 
def login():
    if request.method == 'POST': #post è il metodo del form html che è lo stesso sia per login che per register ma Flask le distingue solo grazie al path della rotta(/login o /register). 
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()  #fetchone() restituisce una riga dalla query. Se la query non ha restituito alcun risultato, restituisce None. 

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):  #check_password_hash() calcola l'hash della password inviata nello stesso modo dell'hash memorizzato e li confronta in modo sicuro
            error = 'Incorrect password.'

        if error is None:  
            session.clear()
            session['user_id'] = user['id'] #La sessione è un dizionario che memorizza i dati tra le richieste. Quando la convalida ha esito positivo, l'ID dell'utente viene memorizzato in una nuova sessione
            #Ora che l'ID dell'utente è memorizzato nella sessione, sarà disponibile per le richieste successive.
            
            return redirect(url_for('weather.index'))
            

        flash(error)

    return render_template('auth/login.html')


#before_app_request significa che **questa funzione viene eseguita prima di ogni richiesta, per tutte le route dell’app, non solo quelle del blueprint.
#Serve per impostare variabili o controllare lo stato dell’utente prima di processare la view.
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')  #Se l'ID non esiste (None), significa che nessuno è loggato.

    if user_id is None:     #Se user_id non esiste → g.user = None (nessuno loggato).

        g.user = None
    else:                   #Se user_id esiste → recuperiamo i dati dell’utente dal database e li salviamo in g.user.
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()
        
        #Non devi recuperare l’utente dal database in ogni singola view: basta leggere g.user.
        #NOTA BENE: g è un ogetto globale di flask mentre g.user è solitamente un dict
        #è possibile configuare g.user come tupla in caso restituisca una sola riga del db
        
        
        
        
#Per disconnettersi, è necessario rimuovere l'ID utente dalla sessione. In questo modo, load_logged_in_user non caricherà più un utente nelle richieste successive.
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('weather.index'))


#Per creare, modificare ed eliminare i post del blog è necessario che l'utente abbia effettuato l'accesso. È possibile utilizzare un decoratore per verificare questa condizione per ogni vista a cui viene applicato.
#Require Authentication in Other Views
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view




#La funzione url_for() genera l'URL di una vista in base a un nome e a degli argomenti. Il nome associato a una vista è anche chiamato endpoint e, per impostazione predefinita, è lo stesso nome della funzione di visualizzazione.
#Quando si utilizza un blueprint, il nome del blueprint viene anteposto al nome della funzione, quindi l'endpoint per la funzione di login che hai scritto sopra è 'auth.login' perché l'hai aggiunta al blueprint 'auth'.


