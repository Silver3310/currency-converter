Currency Converter
==================

A RESTful service to calculate foreign exchange rates (UI is present as well)

.. image:: https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg
     :target: https://github.com/pydanny/cookiecutter-django/
     :alt: Built with Cookiecutter Django

:License: MIT


Prerequisites
-------------
For this project to run you have to make sure you have Python3.7 (or higher), Docker and Docker-Compose installed


Basic Commands
--------------
For your convenience, the file cli.py is created, it contains shortcuts for common commands

* To run the project, run the following commands in terminal::

    $ git clone https://github.com/Silver3310/currency-converter
    $ cd currency-converter
    $ python3 -m venv venv
    $ source venv/bin/activate
    $ pip install click
    $ python cli.py runserver

Now wait for the project to build (for the first time, it may take up to 20-30 minutes) and start using it

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


Creating a super user
~~~~~~~~~~~~~~~~~~~~~~~~~~

To access the admin panel you have to be a super user, you can create one by
::

  $ python cli.py createsuperuser

Screenshots
~~~~~~~~~~~~~~~~~~~~~~~~~~

User interface

.. image:: https://sun4-16.userapi.com/5kvCfkkBy3pehmczejnr8TY6TjLv4Z0Y_x6epQ/IMgn4dPMxxE.jpg

Rest Framework interface

.. image:: https://sun4-15.userapi.com/4GdFMDfyYzlnGbOr-yZ8wVzFyA9iVZBOxmhv3A/baUpBs2ibyI.jpg

