Paranuara Challenge
===================

An API for interplanatory colony information transfer and reporting

.. image:: https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg
     :target: https://github.com/pydanny/cookiecutter-django/
     :alt: Built with Cookiecutter Django

Installing
----------

* Install Requires
    * Python 3
    * Virtualenv & Virtualenvwrapper installed
    * Yarn
    * Postgresql 10+

* Run the following commands ::

    $ git clone git@github.com:sam-mi/paranuara.git
    $ cd paranuara
    $ cp config/settings/local.tmpl.py config/settings/local.py
    $ mkvirtualenv paranuara -p python3
    $ pip install -r requirements/local.txt
    $ yarn (or npm install)
    $ createdb paranuara
    $ ./manage.py migrate
    $ ./manage.py createsuperuser --email admin@paranuara.com --username admin
    $ coverage run ./manage.py test
    $ coverage report -m
    $ ./manage.py runserver

* Navigate to 127.0.0.1:8000/api/
    * Load the list of companies at /api/companies/
    * Load the list of people at /api/people/
    * View a company and its employees at /api/companies/{int}/
    * Compare friends at /api/friends/{int:id}/{int:friend}/

API
---

* ENDPOINTS ::

    /api/
    /api/companies/
    /api/companies/{id}/
    /api/people/
    /api/people/{id}/
    /api/food/
    /api/food/{id}/
    /api/friends/{int:id}/{int:friend}/


Possible Issues
---------------

 - npm or yarn are required, node-sass can cause issues if not working correctly (e.g. after a brew update)
 - coverage is required to run from the virtualenv, it may break if running via a system install
 - on certain systems pythons strftime can behave inconsistently showing a datetime not matching when it should

If any of these issues occur, please let me know so I can help solve them!

Settings
--------

Moved to settings_.

.. _settings: http://cookiecutter-django.readthedocs.io/en/latest/settings.html

Basic Commands
--------------

Setting Up Your Users
^^^^^^^^^^^^^^^^^^^^^

* To create a **normal user account**, just go to Sign Up and fill out the form. Once you submit it, you'll see a "Verify Your E-mail Address" page. Go to your console to see a simulated email verification message. Copy the link into your browser. Now the user's email should be verified and ready to go.

* To create an **superuser account**, use this command::

    $ python manage.py createsuperuser

For convenience, you can keep your normal user logged in on Chrome and your superuser logged in on Firefox (or similar), so that you can see how the site behaves for both kinds of users.

Test coverage
^^^^^^^^^^^^^

To run the tests, check your test coverage, and generate an HTML coverage report::

    $ coverage run manage.py test
    $ coverage html
    $ open htmlcov/index.html

Running tests with py.test
~~~~~~~~~~~~~~~~~~~~~~~~~~

::

  $ py.test

Live reloading and Sass CSS compilation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Moved to `Live reloading and SASS compilation`_.

.. _`Live reloading and SASS compilation`: http://cookiecutter-django.readthedocs.io/en/latest/live-reloading-and-sass-compilation.html





Deployment
----------

The following details how to deploy this application.




