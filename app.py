
import os
import random
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(100), nullable=False, unique=True)

class Verb(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(100), nullable=False, unique=True)

class Object(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(100), nullable=False, unique=True)

import click
from flask.cli import with_appcontext

@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    db.create_all()
    # Pre-populate with some data
    if not Subject.query.first():
        db.session.add(Subject(text="my wife"))
        db.session.add(Subject(text="my dog"))
        db.session.add(Subject(text="our new pet goat"))
        db.session.commit()
    if not Verb.query.first():
        db.session.add(Verb(text="ate"))
        db.session.add(Verb(text="kicked"))
        db.session.add(Verb(text="threw"))
        db.session.commit()
    if not Object.query.first():
        db.session.add(Object(text="laptop"))
        db.session.add(Object(text="mazda"))
        db.session.add(Object(text="cast iron skillet"))
        db.session.commit()
    click.echo('Initialized the database.')

app.cli.add_command(init_db_command)


@app.route('/')
def index():
    subjects = Subject.query.all()
    verbs = Verb.query.all()
    objects = Object.query.all()

    random_subject = random.choice(subjects).text if subjects else ""
    random_verb = random.choice(verbs).text if verbs else ""
    random_object = random.choice(objects).text if objects else ""

    sentence_templates = [
        "Sorry, I can't come out today, because {random_subject} {random_verb} my {random_object}.",
        "Sorry gents, but I'm going to be late because {random_subject} {random_verb} my {random_object}.",
        "Hey dudes,You're not going to believe this, but {random_subject} {random_verb} my {random_object} and I can't come out.",
        "I'm so sorry, but i have to pass tonight since {random_subject} {random_verb} my {random_object}.",
    ]

    sentence_template = random.choice(sentence_templates)
    sentence = sentence_template.format(
        random_subject=random_subject,
        random_verb=random_verb,
        random_object=random_object
    )

    return render_template('index.html', sentence=sentence)

@app.route('/add', methods=['POST'])
def add_word():
    word_type = request.form.get('word_type')
    text = request.form.get('text')

    if not text:
        return redirect(url_for('index'))

    if word_type == 'subject':
        if not Subject.query.filter_by(text=text).first():
            db.session.add(Subject(text=text))
    elif word_type == 'verb':
        if not Verb.query.filter_by(text=text).first():
            db.session.add(Verb(text=text))
    elif word_type == 'object':
        if not Object.query.filter_by(text=text).first():
            db.session.add(Object(text=text))

    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
