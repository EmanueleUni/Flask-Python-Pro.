# -*- coding: utf-8 -*-
"""
Created on Tue Sep 16 16:54:48 2025

@author: Emanuele
"""

import json, os, random

from flaskr.db import get_db

from flaskr.auth import login_required

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

bp = Blueprint('quiz', __name__, template_folder='templates')

file_path = os.path.join(os.path.dirname(__file__), "data", "quiz_data.json")
with open(file_path, "r", encoding="utf-8") as f:
    quiz_data = json.load(f)
    
    #session è un dizionario che contiene i dati della sessione

"""@bp.route("/rank", methods=["GET","POST"])
@login_required
def placement():
    db = get_db()
    
        #quando passi i parametri devono essere una tupla anche se c'è solo un valore sennnò sqlite da errore
        #execute da solo non restituisce il record Devi chiamare .fetchone() o .fetchall()
    
    totPoints=db.execute("SELECT points FROM user WHERE id = ?;", (session.get("user_id"),)).fetchone()
        
    #session.get("user_id") è equivalente a session["user_id"] solo che get() non genera errore se non trova la chiave del dizionario
    if totPoints is None:
        totPoints = {"points": 0}
    
    return render_template("quiz/index.html",totPoints=totPoints )"""

    
@bp.route("/", methods=["GET", "POST"])
@login_required
def start_quiz():
    db = get_db()
    totPoints=db.execute("SELECT points FROM user WHERE id = ?;", (session.get("user_id"),)).fetchone()
    
    if request.method == "POST":
        category = request.form['category']
        # Qui possiamo scegliere 5 domande casuali dalla categoria selezionata
        session["score"] = 0
        session["questions"] = random.sample(quiz_data[category], 5)
        session["current_index"] = 0
        return redirect(url_for("quiz.show_question"))
    # Se è GET, mostra il form per scegliere la categoria  GET: mostra il form per scegliere la categoria
    
    
    d= db.execute(
    "SELECT username,points FROM user",
    ()).fetchall()
    
    return render_template("quiz/index.html", categories=quiz_data.keys(), totPoints=totPoints,d=d)


@bp.route("/question", methods=["GET", "POST"])
@login_required
def show_question():
    questions = session.get("questions", [])
    index = session.get("current_index", 0)

    if index >= len(questions):
        return redirect(url_for("quiz.result"))

    question = questions[index]
    options = question["choices"].copy()
    random.shuffle(options)

    if request.method == "POST":
        selected = request.form.get("answer")
        if selected == question["answer"]:
            session["score"] += 1
        session["current_index"] += 1
        return redirect(url_for("quiz.show_question"))
    
    return render_template("quiz/question.html", question=question, options=options, index=index+1, total=len(questions))


@bp.route("/result")
@login_required
def result():
    db = get_db()
    
    score = session.get("score", 0)
    
    db.execute(
    "UPDATE user SET points = points + ? WHERE id = ?;",
    (score,session.get("user_id")))
    
    db.commit() #db.commit() serve a salvare permanentemente le modifiche nel database.
    
    total = len(session.get("questions", []))
    
    return render_template("quiz/result.html", score=score, total=total) #quando si passa il record deve sempre essere chiave=valore ()


"""
@bp.route("/placement")
@login_required
def placement():
    db=get_db()
    d= db.execute(
    "SELECT username,points FROM user",
    ()).fetchall()
    
    return render_template("quiz/index.html", d=d ) #quando si passa il record deve sempre essere chiave=valore ()

    """

