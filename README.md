# QChat

A Quart based chat

## Setup

### Running with Docker

- Run `docker-compose up --build`
- Open `http://localhost:5000` on your browser
- Run tests by doing `docker-compose run --rm web pipenv run pytest -s`

### MacOS

- Install pipenv `brew install pipenv`
- Install dependencies `pipenv install`
- [Install mongodb](https://docs.mongodb.com/manual/tutorial/install-mongodb-on-os-x/)
- Run mongodb with `mongod --config /usr/local/etc/mongod.conf`
