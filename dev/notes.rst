Running tests
=============
::

    nosetests -vx tests/test_schemas.py # To drop and recreate all the tables
    sh bin/runtests.sh

Frontend build
==============
::

    python fe/build/run.py
    # output goes to pub directory in current directory

Starting Frontend
=================
::

    python fe/run_webserver.py
