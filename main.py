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
from constants import API_KEY

# EndPoin of the Movies API, https://developer.themoviedb.org/docs/search-and-query-for-details
url = "https://api.themoviedb.org/3/search/movie?api_key=" + API_KEY


# Create the Flask app
app = Flask(__name__)
# Configure the secret key for the app (necessary for Flask-WTF)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
# Initialize Bootstrap5 for the Flask app
Bootstrap5(app)


# CREATE DB
class Base(DeclarativeBase):
  pass

# Configure SQLAlchemy with the base model
db = SQLAlchemy(model_class=Base)

# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"

# initialize the app with the extension
db.init_app(app)


# Create the Movie table in the database
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
        # String representation of the Movie object
        return "<Title: {}>".format(self.title)


# Create the database tables within the app context    
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

        
# Main route for the home page
@app.route("/")
def home():
    
    # Get all movies ordered by ranking
    all_movies = db.session.execute(db.select(Movie).order_by(Movie.ranking)).scalars().all()
    
    # Render the 'index.html' template with the list of movies
    return render_template("index.html", movies=all_movies)


# Form class for updating movies
class UpdateForm(FlaskForm):
    
    # Rating field with required input validation
    rating = DecimalField('Rating', [validators.DataRequired(message="Rating is required."), validators.NumberRange(min=1, max=10, message="out of range")])
    
    # Review field with length validation and required input validation
    review = StringField('Review', [validators.Length(min=6, max=35), validators.DataRequired(message="Review is required.")])
    
    # Submit button
    submit = SubmitField('Submit')
    
    

# Route to edit an existing movie
@app.route("/edit/<int:id>", methods=['GET', 'POST'])
def edit(id):
    
    # Create an instance of the update form
    update_form = UpdateForm()
    
    # Get the selected movie by id, or return 404 if not found
    movie_selected = db.get_or_404(Movie, id)
    
    if request.method == 'POST' and update_form.validate():
        
        # Get the form data
        rating = update_form.rating.data
        review = update_form.review.data
        
        print(rating)
        print(review)
        
        # Update the selected movie's data
        movie_selected.rating = rating
        movie_selected.review = review
        
        # Commit the changes to the database
        db.session.commit()
        
        # Redirect to the home page
        return redirect(url_for('home'))
    else:
        # Render the 'edit.html' template with the selected movie and the update form
        return render_template("edit.html", movie=movie_selected, form=update_form)
    
    
# Route to delete an existing movie
@app.route("/delete/<id>")
def delete(id):
    
    # Get the movie to delete by id, or return 404 if not found
    movie_to_delete = db.get_or_404(Movie, id)
    
    # Delete the movie from the database
    db.session.delete(movie_to_delete)
    
    # Commit the changes to the database
    db.session.commit()
    
    # Redirect to the home page
    return redirect(url_for('home'))
  

#form for adding a new movie
class NewMovie(FlaskForm):
    #title of the new movie
    title = StringField(validators=[validators.DataRequired()])
    
    # Submit button
    submit = SubmitField('Submit')

# route for the add page
@app.route("/add",  methods=['GET', 'POST'])
def add():
    
    new_movie_form=NewMovie()
    
    if new_movie_form.validate_on_submit():
        
        new_movie_title=new_movie_form.title.data
        
        print(new_movie_title) 
        
        #NOTE:Using the movie title entered by the user, we make a GET request to the movie API,
        # where we will retrieve the movie information.
        
        parameters={
            'query':new_movie_title
        }
        
        # Making a GET request 
        response = requests.get(url,  params=parameters).json() 

        # Initialize an empty list to store the movie data
        data_list=[]

        # Loop through the results in the JSON response
        for movie in response['results']:
            
            # Create a dictionary for each movie
            data={}
            
            # Add the title and release date to the dictionary
            data['release_date'] = movie['release_date']
            data['title'] = movie['title']
            
            # Append the dictionary to the data_list
            data_list.append(data)
            
            #TODO: RENDERIZAR LA INFORMACION 'MOVIE_DATA' EN SELECT.HTML
        # Redirect to the home page
        return render_template("select.html", movie_data=data_list)
    
    # Render the 'index.html' template with the list of movies
    return render_template("add.html", form=new_movie_form)


if __name__ == '__main__':
    app.run(debug=True)
