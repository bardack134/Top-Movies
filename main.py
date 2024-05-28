from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
from flask_wtf import FlaskForm
from wtforms import DecimalField, StringField, SubmitField
from wtforms.validators import InputRequired 
from wtforms import  StringField, validators
from flask_bootstrap import Bootstrap5
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


# new_movie = Movie(
#     title="Phone Booth",
#     year=2002,
#     description="Publicist Stuart Shepard finds himself trapped in a phone booth, pinned down by an extortionist's sniper rifle. Unable to leave or receive outside help, Stuart's negotiation with the caller leads to a jaw-dropping climax.",
#     rating=7.3,
#     ranking=10,
#     review="My favourite character was the caller.",
#     img_url="https://image.tmdb.org/t/p/w500/tjrX2oWRCM3Tvarz38zlZM7Uc10.jpg"
# )
# second_movie = Movie(
#     title="Avatar The Way of Water",
#     year=2022,
#     description="Set more than a decade after the events of the first film, learn the story of the Sully family (Jake, Neytiri, and their kids), the trouble that follows them, the lengths they go to keep each other safe, the battles they fight to stay alive, and the tragedies they endure.",
#     rating=7.3,
#     ranking=9,
#     review="I liked the water.",
#     img_url="https://image.tmdb.org/t/p/w500/t6HIqrRAclMCA60NsSmeqe9RmNV.jpg"
# )    
# with app.app_context():
#     db.session.add(new_movie)
#     db.session.add(second_movie)
#     db.session.commit()

        
@app.route("/")
def home():
    all_movies = db.session.execute(db.select(Movie).order_by(Movie.ranking)).scalars().all()
    return render_template("index.html", movies=all_movies)


class UpdateForm(FlaskForm):
    rating     = DecimalField('Rating', [validators.DataRequired(message="Rating is required.")])
    
    review       = StringField('Review', [validators.Length(min=6, max=35), validators.DataRequired(message="Review is required.")])
    
    # Submit button
    submit = SubmitField('Submit')
    
    
@app.route("/edit/<int:id>", methods=['GET', 'POST'])
def edit(id):
    
    update_form=UpdateForm()
    
    
    movie_selected = db.get_or_404(Movie, id)
    
    if request.method == 'POST' and update_form.validate():
       
        rating=update_form.rating.data
        review=update_form.review.data
        
        print(rating)
        print(review)
        
        
        #updating data
        movie_selected.rating=rating
        movie_selected.review=review
        db.session.commit()
   
            
        return redirect(url_for('home'))
    else:
        
        return render_template("edit.html", movie=movie_selected, form=update_form)
 
    
@app.route("/delete/<id>")
def delete(id):
     
    movie_to_delete = db.get_or_404(Movie, id)
        
    db.session.delete(movie_to_delete)
    
    db.session.commit()
   
            
    return redirect(url_for('home'))
   
    
        
        


if __name__ == '__main__':
    app.run(debug=True)
