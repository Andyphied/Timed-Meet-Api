# Timed-Meet-Api

This is the Backend for the Timed_Meet Web App.
You can get the proper documentaion of the API [here](https://timed-meet.herokuapp.com/redoc)

## The API Stack:

- Flask (Flask-Smorest)
- Postgres DB
- Heroku

## Some of the great Libaries Used for this Project

- Marhsmallow
- Typing (Python In Built Libary)
- SQLAlchemy

# Setting Up

Open up a terminal and run

### Install virtualenv package

The virtualenv package is required to create virtual environments. You can install it with pip:
`$ pip install virtualenv`

### Create Virtual Environment

To create a virtual environment, you must specify a path. For example to create one in the local directory called .venv, type the following
`$ virtualenv .venv`

### Activate Virtual Environment

You can activate the python environment by running the following command:

- Mac OS / Linux
  `$ source .venv/bin/activate`

- Windows
  `$ .venv\Scripts\activate`

### Install Dependencies

Install all of the dependencies required for the Web App
`$ pip install -r requirements.txt`

### Start Server

Install all of the dependencies required for the Web App
`$ flask run`

## Modifying The API

If further modification is required:

Create a .env file and added the following variables along with their values in it:

- ENVIRON
- FLASK_ENV
- DATABASE_URL
- API_TITLE
- API_VERSION
- JWT_SECRET_KEY

Other variables in .core/config can be tweaked as needed.
