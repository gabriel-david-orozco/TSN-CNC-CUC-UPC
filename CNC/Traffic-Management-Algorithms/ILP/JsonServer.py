from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Create a new Flask application
app = Flask(__name__)

# Set up SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////streams.db'
db = SQLAlchemy(app)

# Define a class for the Artist table
class Streams(db.Model):
    stream_id = db.Column(db.Integer, primary_key=True)
    Source = db.Column(db.String)
    Destination = db.Column(db.String)
    Size = db.Column(db.Integer)
    Period = db.Column(db.Integer)
    Deathline = db.Column(db.Integer)
    Deathline = db.Column(db.Integer)


# Create the table
db.create_all()