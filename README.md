# QChat

A Quart based chat

## Local MySQL server

- Install the packages: `python -m pipenv install`
- Run `python -m pipenv run quart run`
- Open `http://localhost:5000` on your browser
- To open a shell, just do `python -m pipenv run quart shell`
- Run tests by doing `python -m pipenv run pytest`

## Using Docker

- Add the path where this code lives on the Docker client
- Run `docker-compose up --build`
- Open `http://localhost:5000` on your browser
- Run tests by doing `docker-compose run --rm web pipenv run pytest -s`

## Production

- Use Hypercorn `hypercorn --bind 0.0.0.0:$PORT --reload wsgi:app`
