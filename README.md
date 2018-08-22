# StackOverflow-lite

StackOverflow-lite is a platform where people can ask questions and provide answers.

[![Build Status](https://travis-ci.org/KengoWada/Stackoverflow-lite-API.svg?branch=api)](https://travis-ci.org/KengoWada/Stackoverflow-lite-API) [![Maintainability](https://api.codeclimate.com/v1/badges/6cdbe0208a6102b00787/maintainability)](https://codeclimate.com/github/KengoWada/Stackoverflow-lite-API/maintainability) [![Coverage Status](https://coveralls.io/repos/github/KengoWada/Stackoverflow-lite-API/badge.svg?branch=api)](https://coveralls.io/github/KengoWada/Stackoverflow-lite-API?branch=api)

## Getting Started

Clone the project using the [link](https://github.com/KengoWada/Stackoverflow-lite).

### Prerequisites

A browser with the access to the internet.

### Installing

* Clone the project to your local machine
```
git clone https://github.com/KengoWada/Stackoverflow-lite.git
```

### Features

* Post a question
* Post an answer for a particular question
* Get all questions
* Get a single question


### Endpoints

HTTP Method|Endpoint|Functionality
-----------|--------|-------------
POST|api/v1/questions|Create a question
GET|api/v1/questions/questionId|Fetch a specific question
GET|api/v1/questions|Fetch all questions
POST|api/v1/questions/questionId/answers|Add an answer


### Tools Used

* [Flask](http://flask.pocoo.org/) - Web microframework for Python.
* [Virtual Environment](https://virtualenv.pypa.io/en/stable/) - Used to create isolated Python environments
* [PIP](https://pip.pypa.io/en/stable/) - Python package installer.


### Deployment

The API is hosted on [Heroku](https://kengo-stackoverflow-lite-api.herokuapp.com/).

### Built With

* Python/Flask

### Authors

Kengo Wada