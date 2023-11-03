
# Objectiv Backend - Development

Here you'll find instructions for development on the Objectiv Backend. If you want to contribute (Thank you!), please take a look at the [Contribution Guide](https://www.objectiv.io/docs/home/the-project/contribute) in our Docs. It contains information about our contribution process and where you can fit in.

## Setup
```bash
virtualenv venv
source venv/bin/activate
export PYTHONPATH=${PYTHONPATH}:.
export FLASK_APP=objectiv_backend.app
# the following command fails if the postgres lib development headers are not present
# if so, then on ubuntu that can be fixed with: sudo apt-get install libpq-dev
pip install --require-hashes -r requirements.txt
pip install -r requirements-dev.txt
```

## Start DB
```bash
cd ..; docker-compose up --detach objectiv_postgres
cd backend; python objectiv_backend/tools/db_init/db_init.py
```


**SECURITY WARNING:** The above docker-compose command starts a postgres container that allows connections
without verifying passwords. Do not use this in production or on a shared system!

## Start validation service
Using stable docker image:

```bash
docker run -d -p 8082:8082 --rm  --name objectiv_validator objectiv/validator
```

If you have local schema changes, use local version of the validator:
```bash
docker run  -d --rm --name objectiv_validator -p 8082:8082 -v $PWD/../schema/validator:/schema node:16-alpine \
  sh -c 'cd /schema && yarn install && yarn serve'
```

## Run Collector
After setting up the python env, simply run:
```bash
flask run -p 8081
```


## Run Tests and Checks
```bash
pytest tests
mypy objectiv_backend
```

# Build
## Build Container Image
Only requires docker, no python.
```
make docker-image-local
```

## Build Python Package
Requires additional python packages installed: `build` and `virtualenv`
```bash
pip install -r build-requirements.txt
```

Build python package:
```bash
make clean
make python-package
```


# Allowed schema extensions
TODO: update this, and move it to some docs specifically about the taxonomy
* Events:
    * adding new events
    * adding parents to an existing event
    * adding contexts to the requiresContext field of an existing event
* Contexts:
    * adding new contexts
    * adding parents to an existing context
    * adding properties to an existing context
    * adding sub-properties to an existing context (e.g. a "minimum" field for an integer)
