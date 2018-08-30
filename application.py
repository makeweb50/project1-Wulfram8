import os
import requests
import json
import random

from flask import Flask, session, render_template, request, redirect, url_for
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)



# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine("postgres://zzhtcfcgaobuze:038dd636f425caec2d358481d1b5031360dacc04f8849b11ec4b7e19d9ba1b35@ec2-79-125-117-53.eu-west-1.compute.amazonaws.com:5432/dc5t085gj2vk3")
db = scoped_session(sessionmaker(bind=engine))


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        if session.get("login") and session.get("nickname"):
            rnd = random.choice(db.execute("SELECT * FROM books").fetchall())
            res = requests.get("https://www.goodreads.com/book/review_counts.json",
                                params={"key": "MdlurN92OnpSsJSFX19YJQ", "isbns": rnd.isbn})

            context = {
                'avg': res.json()['books'][0]['average_rating'],
                'rnd': rnd,
                'hstr': session["history"]
            }
            return render_template("index.html", cntx = context, nickname = session["nickname"], login = session["login"])
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
            return render_template('registr.html', error='Логин занят')

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

        return render_template('index.html', success=True)

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
            session["id"] = response["id"]
            session["nickname"] = response["nickname"]
            session["login"] = response["login"]
            session["history"] = []
            return redirect(url_for('index'))
        else:
            return render_template('signin.html', error='Неверный логин или пароль')

@app.route("/exit")
def exit():
    session["id"] = ""
    session["nickname"] = ""
    session["login"] = ""
    return redirect(url_for('index'))

@app.route("/book/<isbn>", methods=["GET", "POST"])
def book(isbn):
    if request.method == "GET":
        if not session["id"]:
            return redirect(url_for('signin'))

        book = db.execute("SELECT * FROM books WHERE isbn = :isbn", {"isbn": isbn}).fetchone()
        reviews = db.execute(
            "SELECT text, nickname, rating FROM reviews JOIN users ON users.id=reviews.user_id WHERE reviews.book_isbn=:isbn",
            {"isbn": isbn})
        if book is not None:
            if book in session["history"]:
                session["history"].remove(book)
            if len(session["history"]) > 3:
                session["history"].pop(0)
            session["history"].append(book)
        revUsers = db.execute("SELECT nickname, book_isbn FROM reviews JOIN users ON users.id=reviews.user_id WHERE book_isbn=:isbn AND nickname=:nickname",
                                {"isbn": isbn, "nickname": session["nickname"]}).rowcount == 0
        if book is None:
            return render_template("error.html", message="No book")
        res = requests.get("https://www.goodreads.com/book/review_counts.json",
                            params={"key": "MdlurN92OnpSsJSFX19YJQ", "isbns": isbn})
        if res.status_code == 200:
            gr = {'average': "", 'rcount': ""}
            gr['average'] = res.json()['books'][0]['average_rating']
            gr['rcount'] = res.json()['books'][0]['work_ratings_count']
            return render_template("book.html", kom=revUsers, reviews=reviews, gr=gr, book=book,
                                    nickname = session["nickname"], login = session["login"])
        else:
            return render_template("book.html", kom=revUsers, reviews=reviews, book=book,
                                    nickname = session["nickname"], login = session["login"])
    if request.method == "POST":
        if session["id"]:
            review_text = request.form.get("review")
            rating = request.form.get("rating")
            db.execute("INSERT INTO reviews (text, user_id, book_isbn, rating) VALUES (:review, :user_id, :isbn, :rating)",
                        {"review": review_text, "user_id": session["id"], "isbn": isbn, "rating": rating})
            db.commit()
            return redirect(url_for('book', isbn=isbn))


@app.route("/api/<isbn>", methods=["GET"])
def api(isbn):
    ares = {
        "title": "",
        "author": "",
        "year": 0,
        "isbn": "",
        "review_count": "Service unavailable",
        "average_score": "Service unavailable"
    }
    res = requests.get("https://www.goodreads.com/book/review_counts.json",
                            params={"key": "MdlurN92OnpSsJSFX19YJQ", "isbns": isbn})
    bres = db.execute("SELECT * FROM books WHERE isbn = :isbn", {"isbn": isbn}).fetchone()
    if not bres:
        return render_template('error.html', message='404. Not found'), 404

    ares["title"] = bres.title
    ares["author"] = bres.author
    ares["year"] = bres.year
    ares["isbn"] = bres.isbn
    if res.status_code == 200:
        ares["review_count"] = res.json()['books'][0]['work_ratings_count']
        ares["average_score"] = res.json()['books'][0]['average_rating']

    return json.dumps(ares)
