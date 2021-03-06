FROM python:3.9-slim

# Install ImageMagick for Wand
RUN apt-get update && apt-get install -y
RUN apt-get install -y \
    imagemagick \
    libmagickwand-dev

# Install pipenv
RUN pip install pipenv

## make a local directory
RUN mkdir /qchat_app

# set "counter_app" as the working directory from which CMD, RUN, ADD references
WORKDIR /qchat_app

# now copy all the files in this directory to /code
ADD . .

# pipenv install
RUN pipenv install

# Listen to port 5000 at runtime
EXPOSE 5000

# Define our command to be run when launching the container
CMD pipenv run quart run --host 0.0.0.0
