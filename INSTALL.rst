superuser tasks
================
::

    sudo bash
    apt-get install libevent-dev python-dev git postgresql python-psycopg2 python-virtualenv rubygems python-turbomail ruby curl
    gem install compass # for dev setups only
    gem install compass-susy-plugin # for dev setups only
    su - postgres
    createuser -S -d -R -P <login-user>
    ^d # back as superuser 
    ^d # back as initial user
    createdb <db-name>
    

Development env setup
=====================
::

    virtualenv apphome
    cd apphome
    . ./bin/activate
    git clone git@github.com:Cowoop/cowspa3.git # Writable
    git clone git://github.com/Cowoop/cowspa3.git # Read only
    cd cowspa3
    # wget https://bitbucket.org/dvarrazzo/psycogreen/raw/77a9c05f5229/gevent/psyco_gevent.py
    pip install -r requirements.txt
    pip install -r dev-requirements.txt # optional packages useful in cowspa3 development
    bash wkhtmltox-installer.sh
    vi conf_dev.py # Refer conf_default.py
    vi conf_test.py 

    # Admin account setup
    python bin/setup.py

    # Frontend build
    python fe/build/run.py

    # Start web server
    python fe/run_webserver.py -h
    python fe/run_webserver.py -d -c test

    # UI
    # firefox http://127.0.0.1:5001


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
