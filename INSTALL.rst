superuser tasks
================
::

    sudo bash
    apt-get install libevent-dev python-dev git postgresql python-psycopg2 python-virtualenv
    su - postgres
    createuser -S -d -R -P <login-user>
    ^d # back as superuser 
    ^d # back as initial user
    createdb <db-name>
    

Development env setup
=====================
::

    git clone git@github.com:shon/cowspa3.git # Writable
    git clone git://github.com/shon/cowspa.git # Read only
    virtualenv cowspa3
    cd cowspa3
    . ./bin/activate
    pip install -r requirements.txt
    pip install -r dev-requirements.txt # optional packages useful in cowspa3 development
    vi conf_dev.py # Refer conf_default.py
    vi conf_test.py 

shell
-----
ipython::

    >>> import be.bootstrap
    >>> be.bootstrap.start('conf_dev')

Tests
-----
::

    nosetests -v tests/test_schemas.py tests/test_bases.py
    # ^ are some basic tests, there are more tests in tests/

Python 3 Notes # SKIP THIS FOR NOW
==================================
::

    sudo apt-get install python3-dev python-virtualenv
    virtualenv cowspa3
    cd cowspa3
    . ./bin/activate
    # wget https://bitbucket.org/rafacv/werkzeug-python3/get/tip.tar.bz2 # This werkzeug does not work
    # pip install tip.tar.bz2
    wget https://download.github.com/ipython-ipython-py3k-9c4fead.tar.gz
    pip install ipython-ipython-py3k-9c4fead.tar.gz
