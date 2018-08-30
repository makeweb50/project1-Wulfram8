# Project 1

Web Programming with Python and JavaScript

И так сайт про книги. На этот раз он выглядит лучше, по крайней мере с моей точки зрения.

В /templates находятся шаблоны для рендера пока что их 6 это "index.html" для главной(и еще для нескольких страниц), "registr.html" и "signin.html" соответсвенно для страниц регистрации и входа, "book.html" для страницы с отдельной книгой, "error.html" для вывода ошибок(оказывается в фреймворках есть своя реализация для этого но кто же знал), "layout.html" шаблон шаблонов? короче чтобы не прописывать одно  и тоже во всех страницах.

В /static находятся всякие доп файлы типа изображений, стилей css и js кода...

В файле /application.py прописан сервер. В /import.py небольшая программа для добавления данных из "book.csv" в базу данных.

Использовалась база данных PostgreSQL с таблицами:

books (
    id SERIAL PRIMARY KEY,
    isbn VARCHAR UNIQUE,
    title VARCHAR NOT NULL,
    author VARCHAR NOT NULL,
    year VARCHAR NOT NULL,
);

users (
    id SERIAL PRIMARY KEY,
    login VARCHAR UNIQUE,
    password VARCHAR NOT NULL,
    nickname VARCHAR
);

reviews (
    id SERIAL PRIMARY KEY,
    text VARCHAR,
    user_id INTEGER REFERENCES users(id),
    book_isbn VARCHAR REFERENCES books(isbn),
    rating INTEGER NOT NULL
);
