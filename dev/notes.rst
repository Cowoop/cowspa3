Activating env
==============
You need to initialize development environment before doing any of the tasks below sections

::

    . bin/activate
    cd cowspa3

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
