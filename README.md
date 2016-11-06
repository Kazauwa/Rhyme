# Rhyme
Things that rhyme with your music taste

## Description

A simple web app which helps user to gather all his favourite music (or rather covers) in one place. In addition Rhyme can make trivial 
recommendations based on other people's collections with similar tastes.

Database is powered by Discogs

## Usage

Set up a virtual environment, install dependencies from requirements.txt
`pip install -r requirements.txt`

Set up environment variables **FLASK_SECRET** (any string) and **SQLALCHEMY_DATABASE_URI**

Create a database (you'll have to do this manually), then initialize it, running in terminal
```
./manage.py db init
./manage.py db migrate
./manage.py db upgrade
```
That's it! You are ready to start! Run `./manage.py runserver` in terminal to start application

## Managing

Currently manage.py can only run the application and manage migrations. More functions will be added in future. 

For managing migrations read the [official documentation] (https://flask-migrate.readthedocs.io/en/latest/)
