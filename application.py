import os
import requests

from flask import Flask, session, render_template, request, redirect, url_for
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        if session["login"] and session["nickname"]:
            return render_template("index.html", nickname = session["nickname"], login = session["login"])
        return render_template("index.html")
    if request.method == "POST":
        search = request.form.get("search")
        ksearch = '%' + search + '%'
        result = db.execute("SELECT * FROM books WHERE to_tsvector(author) || to_tsvector(title) @@ plainto_tsquery(:search) OR isbn LIKE :ksearch",
            {"search": search, "ksearch": ksearch})
        return render_template("index.html", search=search, result = result, nickname = session["nickname"], login = session["login"])

@app.route("/registration", methods=["GET", "POST"])
def registr():
    if request.method == "GET":
        return render_template("registr.html")
    if request.method == "POST":
        nickname = request.form.get("nickname")
        login = request.form.get("login")
        password = request.form.get("password")

        if db.execute("SELECT * FROM users WHERE login = lower(:login)", {"login": login}).rowcount != 0:
            return "Login zanyat"

        if login and password:
            if not nickname:
                db.execute("INSERT INTO users (login, password, nickname) VALUES (lower(:login), :password, :nickname)",
                    {"login": login, "password": password, "nickname": login})
            else:
                db.execute("INSERT INTO users (login, password, nickname) VALUES (lower(:login), :password, :nickname)",
                    {"login": login, "password": password, "nickname": nickname})
            db.commit()
        else:
            return render_template('error.html', message='400, Bad request'), 400

        return render_template('success.html', message="You sign up!")

@app.route("/signin", methods=["GET", "POST"])
def signin():
    if request.method == "GET":
        return render_template("signin.html")
    if request.method == "POST":
        login = request.form.get("login")
        password = request.form.get("password")
        response = db.execute("SELECT * FROM users WHERE login = lower(:login) AND password = :password",
            {"login": login, "password": password}).first()

        if response:

            session["nickname"] = response["nickname"]
            session["login"] = response["login"]
            return redirect(url_for('index'))
        else:
            return render_template('error.html', message='Такого пользователя нет')

@app.route("/exit")
def exit():
    session["nickname"] = ""
    session["login"] = ""
    return redirect(url_for('index'))

@app.route("/book/<isbn>")
def book(isbn):
    book = db.execute("SELECT * FROM books WHERE isbn = :isbn", {"isbn": isbn}).fetchone()
    if book is None:
        return render_template("error.html", message="No book")
    res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "MdlurN92OnpSsJSFX19YJQ", "isbns": isbn})
    if res.status_code == 200:
        gr = {'average': "", 'rcount': ""}
        gr['average'] = res.json()['books'][0]['average_rating']
        gr['rcount'] = res.json()['books'][0]['work_ratings_count']
        return render_template("book.html", gr=gr, book=book)
    else:
        return render_template("book.html", book=book)
