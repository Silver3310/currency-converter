Currency Converter
==================

A project to calculate foreign exchange rates

.. image:: https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg
     :target: https://github.com/pydanny/cookiecutter-django/
     :alt: Built with Cookiecutter Django

:License: MIT


Prerequisites
-------------
For this project to run you have to make sure you have Docker and Docker-Compose installed


Basic Commands
--------------
For your convenience, the file cli.py is created, it contains shortcuts for common commands

* To run the project, run the following commands in terminal::

    $ python3 -m venv venv
    $ source /venv/bin/activate
    $ pip install click
    $ python cli.py runserver

Now wait for the project to build and start

Type checks
^^^^^^^^^^^

Running type checks with mypy:

::

  $ python cli.py mypy

Test coverage
^^^^^^^^^^^^^

To run the tests, check your test coverage, and generate an HTML coverage report::

    $ python cli.py cov
    $ open htmlcov/index.html

Running tests with py.test
~~~~~~~~~~~~~~~~~~~~~~~~~~

::

  $ python cli.py test
