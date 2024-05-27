from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests


# create the app
app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)

# CREATE DB
class Base(DeclarativeBase):
  pass
db = SQLAlchemy(model_class=Base)

# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"

# initialize the app with the extension
db.init_app(app)


# CREATE TABLE
class Movie(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    year= db.Column(db.Integer,  nullable=False)
    description= db.Column(db.String(250),  nullable=False)
    rating= db.Column(db.Float,  nullable=False)
    ranking= db.Column(db.Integer,  nullable=False)
    review= db.Column(db.String(250),  nullable=False)
    img_url= db.Column(db.String(250),  nullable=False)

    def __repr__(self):
        return "<Title: {}>".format(self.title)
    
with app.app_context():
    db.create_all()

    

        
@app.route("/")
def home():
    all_movies = db.session.execute(db.select(Movie).order_by(Movie.ranking)).scalars().all()
    return render_template("index.html", movies=all_movies)


if __name__ == '__main__':
    app.run(debug=True)
