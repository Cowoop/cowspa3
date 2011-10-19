Installing Windmill
-------------------

Go to your virtualenv setup (optional)::

    pip install windmill

Firefox without Default Profile
-------------------------------

firefox needs to have a default profile, else you'll run into an error.
To address this error, Edit <homedir>/.windmill/prefs.py , Add the following lines ::

    MOZILLA_BINARY='path/to/firefox.exe'
    MOZILLA_DEFAULT_PROFILE='path/to/firefox/profiles'

Executing the Windmill test cases
---------------------------------

To executes the test cases, Go to ...../cowspa3/tests/fe_tests ::

    nosetests --wmbrowser firefox -v -d --with-xunit

Output is available by default in **nosetests.xml** This file contains the test results. If needed, the output can be sent to another file.
The XML output can be used to generate HTML report using following command ::

    python xunit2html.py > nose_result.html

Tests can also be executed via windmill binary as follows, but executing via nose is preferred due to the detailed report it provides ::

    windmill -m test=test_cowspa.py exit

