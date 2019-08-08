Paranuara Challenge
===================

An API for interplanatory colony information transfer and reporting

Installing
----------

* Install Requires
    * Python 3
    * Virtualenv & Virtualenvwrapper installed
    * Postgresql 10+

* Run the following commands ::

    $ git clone git@github.com:sam-mi/paranuara.git
    $ cd paranuara
    $ mkvirtualenv paranuara -p python3
    $ pip install -r requirements/local.txt
    $ createdb paranuara
    $ ./manage.py migrate
    $ ./manage.py runserver

* Visit 127.0.0.1:8000/api/

    * POST the list of companies at /api/companies/
    * POST the list of people at /api/people/
    * If a Company is referenced in the people.json data that doesn't exist it will throw a 404 with a message showing the missing company.id and the person.id for the failing row. This is done to maintain referential integrity of the loaded data.
    * View a company and its employees at /api/companies/{int}/
    * Compare friends at /api/friends/{int:id}/{int:friend}/
    * View food at /api/food/

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



Notes
-----

- Settings are located at `config/settings/base.py` & `config/settings/local.py`
- Due to simplification admin and auth etc no longer work.
- Due to the structure of the data, that a Person object has a foreign key to Company, its necessary to post companies before posting people.
- Friends indicate an m2m relationship from Person to self, this means that some friends won't exist when they are being assigned, to handle this the ids are saved to a _friend_cache json field, calls to Person.update_friends will add missing friends, it's called on create and upon comparing friends. An endpoint could be created to force update, or a management command if necessary, or both.

Possible Issues
---------------

 - company ids count from 0 while person.company_id counts from 1, this may cause problems (i.e. there is no company_id with id 100, however it is referenced 10x in the person.json - the api will throw a 404 with a helpful message).
 - npm or yarn are required, node-sass can cause issues if not working correctly (e.g. after a brew update).
 - coverage is required to run from the virtualenv, it may break if running via a system install.
 - on certain systems pythons strftime can behave inconsistently showing a datetime not matching when it should, this may be caused by having supervisorctl or supervisor installed.

If any of these issues occur, please let me know so I can help solve them!


Test coverage
^^^^^^^^^^^^^

To run the tests, check your test coverage, and generate an HTML coverage report::

    $ coverage run manage.py test
    $ coverage html
    $ open htmlcov/index.html



