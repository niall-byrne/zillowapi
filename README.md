# Zillow API

Reads Zillow CSV Files, and Serves Them Via an API

![zillowapi Automation](https://github.com/niall-byrne/zillowapi/workflows/zillowapi%20Automation/badge.svg)

## Development Dependencies

You'll need to install:
 - [Docker](https://www.docker.com/) 
 - [Docker Compose](https://docs.docker.com/compose/install/)

## Setup the Development Environment

Build the development environment container (this takes a few minutes):
- `docker-compose build`

Start the environment container:
- `docker-compose up -d`

Spawn a shell inside the container:
- `./container`

Access the API:

- [http://localhost:8000/api/](http://localhost:8000/api/)

## API Reference

Navigate to the redoc endpoint:

[http://localhost:8000/redoc/](http://localhost:8000/redoc/)

## Loading CSV Content

Copy the test data to the Git repository folder you cloned, and it will be accessible inside the container.
- `./manage.py load_csv [filename]`

## CLI Reference
The CLI is enabled by default inside the container, and is also available on the host machine.

```
$ dev
Valid Commands:
 - lint
 - lint-validate
 - reinstall-requirements
 - sectest
 - setup
 - test
 - test-coverage
```
