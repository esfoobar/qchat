# QChat

A Quart based chat

## Setup

### Running with Docker

- Run `docker-compose up --build`
- Open `http://localhost:5000` on your browser
- Run tests by doing `docker-compose run --rm web pipenv run pytest -s`

### MacOS

- Install pipenv `pip install pipenv`
- Install dependencies `pipenv install`
  - You will need to install ImageMagick dependency via `brew install imagemagick`
- [Install mongodb](https://docs.mongodb.com/manual/tutorial/install-mongodb-on-os-x/)
  - `brew tap mongodb/brew`
  - `brew install mongodb-community@5.0`
- Run mongodb with `mongod --config /usr/local/etc/mongod.conf --fork`
- Set the mongodb host on `.quartenv` to `localhost`
- Run the application using `pipenv run quart run --host 0.0.0.0`

### Windows

- Install pipenv `pip install pipenv`
- Install dependencies `pipenv install`
  - You will need to install ImageMagick dependency via `winget install imagemagick`
- [Install mongodb](https://docs.mongodb.com/manual/tutorial/install-mongodb-on-windows/)
  - ` winget install "MongoDB Server"`
  - Create a directory called `\data\db` with `md "\data\db"`
- Run mongodb with `C:\"Program Files"\MongoDB\Server\5.0\bin\mongod.exe --dbpath="c:\data\db"` (note the double quotes around "Program Files")
- Set the mongodb host on `.quartenv` to `localhost`
- Run the application using `pipenv run quart run --host 0.0.0.0`
- Allow Windows Defender Firewall access
