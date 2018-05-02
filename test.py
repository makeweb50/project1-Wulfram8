import os
import requests

from flask import Flask, session, render_template, request, redirect, url_for
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "MdlurN92OnpSsJSFX19YJQ", "isbns": "1416949658"}).json()
print(res)
