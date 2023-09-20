from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
Bootstrap5(app)
db = SQLAlchemy()
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///movies.db"
db.init_app(app)
API_KEY = os.getenv("API_KEY")


# Creating a table for the database entry
class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True, nullable=False)
    year = db.Column(db.Integer)
    description = db.Column(db.String(500), nullable=False)
    rating = db.Column(db.Float, nullable=True)
    ranking = db.Column(db.Integer, nullable=True)
    review = db.Column(db.String(250), nullable=True)
    img_url = db.Column(db.String(250), nullable=False)


with app.app_context():
    db.create_all()


# Form for Rating movies
class RateMovieForm(FlaskForm):
    rating = StringField("Your rating out of 10 e.g 7.5")
    review = StringField("Your review")
    done = SubmitField('Done')

# form for add movie section
class AddMovie(FlaskForm):
    title = StringField('Movie Title')
    add = SubmitField('Add Movie')

# Database manual entry.. deprecated
"""
with app.app_context():
    new_movie = Movie(
        title="Avatar the way of water",
        year=2022,
        description="Set more than a decade after the events of the first film, "
                    "learn the story of the Sully family (Jake, Neytiri, and their kids), "
                    "the trouble that follows them, the lengths they go to keep each other "
                    "safe, the battles they fight to stay alive, and the tragedies they endure.",
        rating=7.3,
        ranking=9,
        review="I like the water.",
        img_url="https://image.tmdb.org/t/p/w500/t6HIqrRAclMCA60NsSmeqe9RmNV.jpg"

    )
    db.session.add(new_movie)
    db.session.commit()
"""

# Flask app sections - HOME
@app.route("/", methods=['GET'])
def home():
    result = db.session.execute(db.select(Movie))
    all_movie = result.scalars()
    return render_template("index.html", movies=all_movie)


# Flask app sections - RATE MOVIE PAGE
@app.route('/edit', methods=['GET', 'POST'])
def rate_movie():
    form = RateMovieForm()
    movie_id = request.args.get('id')
    print(movie_id)
    # either of the two expression to select the form row is valid before the validation line
    # movie = db.get_or_404(Movie, movie_id)
    movie = db.session.execute(db.select(Movie).where(Movie.id == movie_id)).scalars()
    if form.validate_on_submit():
        movie.rating = float(form.rating.data)
        movie.review = form.review.data
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('edit.html', form=form, movie=movie)


# Flask app sections - DELETE MOVIE FUNCTION
@app.route('/delete', methods=['GET', 'POST'])
def delete_movie():
    movie_id = request.args.get('id')
    movie = db.get_or_404(Movie, movie_id)
    db.session.delete(movie)
    db.session.commit()
    return redirect(url_for('home'))


# Flask app sections - ADD NEW MOVIE PAGE
# Moviedb API request
endpoint = "https://api.themoviedb.org/3/search/movie?include_adult=false&language=en-US&page=1"
header = {
    "accept": "application/jason",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIzZmYwMTcxOWNmMWI3ZjU1MmQ5M2ExMTgxYTc1ZTdkZSIsInN1YiI6IjY1MDQ3NDA5YjUxM2E4MDBjNmMxNWQ4YyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.0skyLMo6uPK7L6WdkKz-n-O5fGVX5pHwoaasRz0p5VE"
}

@app.route('/add', methods=['GET', 'POST'])
def add_movie():
    form = AddMovie()
    if form.validate_on_submit():
        movie_title = form.title.data
        response = requests.get(endpoint, params={"api_key": API_KEY, "query": movie_title})
        data = response.json()['results']
        return render_template('select.html', movies=data)
    return render_template('add.html', form=form)



# Api fetching the selected movie
img_base_url = "https://image.tmdb.org/t/p/w500"
api_endpoint = "https://api.themoviedb.org/3/movie/"
@app.route('/find')
def find_movie():
    movie_id = request.args.get('id')
    if movie_id:
        movie_api_url = f"{api_endpoint}{movie_id}"
        response = requests.get(url=movie_api_url, params={"api_key": API_KEY, "language": "en-US"})
        data = response.json()
        new_movie = Movie(
            title=data['title'],
            year=data['release_date'].split('-')[0],
            img_url=f"{img_base_url}{data['poster_path']}",
            description=data["overview"]
        )
        db.session.add(new_movie)
        db.session.commit()
        return redirect(url_for('rate_movie', id=movie_id))


if __name__ == '__main__':
    app.run(debug=True)

