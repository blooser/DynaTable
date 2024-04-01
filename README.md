# DynaTable 🚀

![CI Status](https://github.com/blooser/DynaTable/actions/workflows/docker-image.yml/badge.svg)

DynaTable is an innovative dynamic model builder tailored for Django, equipped with a potent REST API interface. It facilitates the on-the-fly creation, updating, and management of database models 🌟. Crafted meticulously using Django, Django REST Framework, and PostgreSQL, DynaTable stands as an indispensable asset for applications necessitating versatile and dynamic database schema management.

## Technologies 💻
- [Python](https://www.python.org/)
- [Django](https://www.djangoproject.com/) + [Django REST Framework](https://www.django-rest-framework.org/)
- [PostgreSQL](https://www.postgresql.org/)
- [Docker](https://www.docker.com/)
- [Swagger](https://swagger.io/) and [Redoc](https://redoc.ly/)
- [Pytest](https://docs.pytest.org/en/stable/)


## Core Features 🌈

- **Dynamic Model Creation** 🛠️: Intuitively define and instantiate new database models via a RESTful interface.
- **Model Schema Updates** 🔧: Seamlessly modify existing models' schemas without the need to adjust the underlying codebase.
- **Efficient Data Manipulation** 📊: Dynamically insert and retrieve data rows for any constructed model.
- **RESTful API Excellence** 🌐: Capitalize on the robust functionality of Django REST Framework for streamlined API interactions.
- **PostgreSQL Integration** 💾: Guarantee strong and dependable data storage solutions with PostgreSQL.

## Build and Run 🏗️

### Building the Application

```bash
$ docker-compose build
```

###  Running the Application

```bash
$ docker-compose up -d
```

## Multi-stage Build 🛠️

DynaTable employs a sophisticated multi-stage building process, encapsulated within Docker for optimal efficiency and performance.

## Exploring API Documentation with Swagger/Redoc 📚

DynaTable simplifies API documentation exploration by utilizing both Swagger and Redoc.

Navigate to:

- Swagger UI

```bash
http://localhost:8000/swagger
```

- Redoc

```bash
http://localhost:8000/redoc
```

## Unit Testing with Pytest 🧪

The application boasts comprehensive unit test coverage utilizing Pytest.

Execute unit tests with:

```bash
$ $ docker-compose run test
```

## Advanced Data Generation and Testing 🔍

DynaTable rigorously tests its functionalities using Pytest alongside generated data, ensuring maximum effectiveness. The bespoke [generator](https://github.com/blooser/DynaTable/blob/master/src/tests/generator.py) module proficiently produces random model fields and data rows for database population. This ensures diverse testing scenarios and enhances the overall quality and reliability of the functions.

# License

This project is licensed under the MIT License - view the [LICENSE.md](https://github.com/blooser/DynaTable/blob/master/LICENSE.md) file for details.
