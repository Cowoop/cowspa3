Design goals
==================

- Moeular code, clear code layers seperation especially frontend and backend
- Web framework agnostic
- Make API exposing and publishing easier
- Reasonably fast on commodity hardware
- scale horizontally without added complexities

High level design
=================

This is multitier architecture like most modern applications.

Here is a simplistic view

::



    |            +--------------+       +-------------+    +------------+                       # planned
    |            |  bases       |       |  commonlib  |    |  libs      |
    |            |--------------|       |-------------|    |------------|
    |            |              |       |             |    |            |   +------------------------------+
    |            +--------------+       +-----+-------+    +------------+   | Repository Layer             |
    |                                         |                 ^           |                              |
    |                                         v *               |           |   +--------+                 |
    |                                                           |           |   |dbaccess|                 |
    |     +--------------+                +---------+    +------+------+    |   |--------|                 |
    |     |      UI      |                |         |    |  APIs(Logic)|    |   |        |                 |
    |     |--------------|                |         |    |-------------|    |   |        |                 |
    |     |              |                |Publisher|    |             |    |   |        |                 |
    |     |              |+-------------->|   /     |+-->|- membership |+-----> |        |                 |
    |     |              |  jsonrpc 2.0   |Dispatch |    |- invoicing  |    |   |        |                 |
    |     |              |                |         |    |- booking    |    |   +--------+                 |
    |     |              |                |         |    |             |    |                    +-------+ |
    |     |              |                |         |    |             |    |   +--------+       |DB     | |
    |     +--------------+                +---------+    +-+-+-----+---+    |   |stores  |       |drivers| |
    |           ^                            ^    ^                |        |   |--------|       |-------| |
    |           |                            |    |                |        |   |        |       |psycopg| |
    |           |          +-----------------+    |                +----------->|        |+----->|       | |
    |           |          |                      |                         |   |        |       |redis #| |
    |         +-+----------+----+                 |                         |   |        |       |       | |
    |         |   Tests         |                 |                         |   +--------+       +-------+ |
    |         |-----------------|                 |                         +------------------------------+
    |         |                 |                 |
    |         +-----------------+                 |
    |                                +------------------------------------------------+
    |                                |                                                |
    |                                | API Docs generators, Task Queues, Hooks, Event |
    |                                | subscriptions, cache #                         |
    |                                |                                                |
    |                                +------------------------------------------------+

.. http://nightly.ascii-flow.appspot.com/#200662316637095930/1192973486
.. http://nightly.ascii-flow.appspot.com/#200662316637095930


Layers and important components
===============================

Bases
-----
Bases are Abstract base classes describing interfaces to be implemented by various components.

API Layer
----------
All features/functions of the product has module that contains entry points for respective function. All APIs are callables (functions/methods). Every functionality provide set of APIs for resource and collection which are loosely inspired REST style architectures. 

Example

invoice module provide function new that created new invoice. 

Ref: See be.apis.invoice.new .

These APIs further arranged in logical namespace which unlitimately help application composition. This application is (currently) exposed using JSONRPC 2.0 publisher. 

Ref: See be.apps .

Accessing APIs in Python shell
-------------------------------
python::

    >>> import be.bootstrap
    >>> be.bootstrap.start('conf_dev')
    >>> import be.apis.usage as usagelib
    >>> info = usagelib.usage_resource.info(808)


Repository layer
----------------
code directory: be/repository

Repository layer abstracts all database interactions and also provides object stores. Object stores implement interface as defined by bases.persistence.BaseStore . It is possible for a object store to use different database engines that implement BaseStore.

Application
-----------
Application is composed using APIs organized as per functionality modules.

User Interface (Web)
--------------------
Web frontend is essentially JSONRPC client of the application. All html pages are build built using frontend build scripts. All pages are generated like static html pages and build output is stored in pub/ directory. This is frontend build produces static pages and webserver agnostic. These pages can be served by fast static resources serving specialized http server (eg. nginx). Once page is served jsonrpc client requests for data and acts accordingly. `Knockout.js <http://knockoutjs.com/>`_ library is used produce rich, responsive pages that updates dynamically as per underlying data model changes.

Codebase organization
---------------------

Top level directories
---------------------

::

    .
    ├── bases           // Abstract base classes
    ├── be              // backend
    ├── fe              // frontend
    ├── commonlib       // utilities, definitions shared across layer
    ├── tests           // test
    │

Backend code organization
-------------------------

::

    be                  // backend top level directory
    ├── bootstrap.py    // initialize env
    ├── apps.py         // application composition and publishing
    ├── wrappers.py     // API wrappers
    │
    ├── apis            // modules containing APIs for all business objects and application logic
    │   ├── invoice.py
    │   ├── usage.py
    │   :
    │
    ├── libs            // helper backend libraries
    │   ├── cost.py
    │   ├── macros.py
    │   :
    │
    ├── repository      // persistance
    │   ├── access.py
    │   ├── pgdb.py     // postgres pool
    │   └── stores.py   // schema for stores
    │
    ├── templates       // templates currently invoice template
    │   ├── invoice.py
    │   ├── scss        // style
    │   :

Key packages/libraries used
=============================

Python
------

- psycopg2
- flask
- Gevent
- nosetests
- `sphc <http://pypi.python.org/pypi/sphc>`_
- jsonrpc

More at requirements.txt and dev-requirements.txt


Javascript
----------

- Jquery
- Jquery UI
- `Knockout.js <http://knockoutjs.com/>`_

More at fe/contrib/README
