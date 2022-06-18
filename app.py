
from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy
# from flask_restful import reqparse
import os


app = Flask(__name__)

uri = os.getenv("DATABASE_URL")
if uri and uri.startswith("postgres://"):
    uri= uri.replace("postgres://", "postgresql://", 1)
    app.config['SQLALCHEMY_DATABASE_URI'] = uri
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://tobi:1234@localhost:5432/movies'

db = SQLAlchemy(app)

# create table
# ORM - Object Relational Mapping


class Movie(db.Model):
    __tablename__ = "movie"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    release_date = db.Column(db.String, nullable=False)
    rating = db.Column(db.Integer, nullable=True)
    num_of_raters = db.Column(db.Integer, default=0)

    def __repr__(self) -> str:
        return f'<Movies {self.name}>'


db.create_all()


# endpoint
@app.route('/movies')
def get_all_movies():
    movies = Movie.query.all()
    all_movie = [{
        "id": m.id,
        "name": m.name,
        "release_date": m.release_date, 
        "rating":m.rating,
        "num_of_raters":m.num_of_raters
        } for m in movies]
    return jsonify({"movies": all_movie})



@app.route("/movies/create", methods=['POST'])
def create_movie():
    movie_req = request.get_json()
    movie_data = {
        'name':movie_req.get('name', ""),
        'release_date':movie_req.get('release_date', ''),
        'rating': movie_req.get('rating', 0),
        'num_of_raters':movie_req.get('num_of_raters', 0) 
        

    }
    movie = Movie(**movie_data)
    db.session.add(movie)

    db.session.commit()
    return jsonify({"message":"successful"})


@app.route('/')
def home():
    return render_template('index.html', movies=Movie.query.all())


if __name__ == "__main__":
    app.run(debug=True)
