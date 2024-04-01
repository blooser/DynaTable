# DynaTable 🚀

![CI Status](https://github.com/blooser/DynaTable/actions/workflows/docker-image.yml/badge.svg)

DynaTable is a dynamic model builder for Django, providing a powerful REST API interface for creating, updating, and managing database models on the fly 🌟. Built with Django, Django REST Framework, and PostgreSQL, DynaTable is the ideal tool for applications requiring flexible and dynamic database schema management.

## Technologies
- Python
- Django + Django REST
- Postgresql
- Docker
- Swagger and Redoc
- Pytest
- Generator


## Features 🌈

- **Dynamic Model Creation** 🛠️: Easily define and create new database models through a RESTful interface.
- **Model Schema Updates** 🔧: Update existing models' schema without altering your underlying codebase.
- **Data Manipulation** 📊: Insert and retrieve rows dynamically for any created model.
- **RESTful API** 🌐: Leverage the power of Django REST Framework for seamless API interactions.
- **PostgreSQL Integration** 💾: Robust and reliable data storage with PostgreSQL.


## Build and run

To build application

```bash
$ docker-compose build
```

Run

```bash
$ docker-compose up -d
```

### Multi-stage build

DynaTable is packed into docker and uses multi-stage approach.


### Swagger/Redoc

DynaTable gives you easy way to check API documentation. It uses both `swagger` and `redoc`

To navigate:

*Swagger*

```
http://localhost:8000/swagger
```

*redoc*

```
http://localhost:8000/redoc
```

### Unit test

The application is covered with unit test.

To execute unit test

```bash
$ docker-compose run test
```

## Generator and multiple invoke

...

# Contributing

Please read CONTRIBUTING.md for details on our code of conduct, and the process for submitting pull requests to us.

# License

This project is licensed under the MIT License - see the LICENSE.md file for details.
