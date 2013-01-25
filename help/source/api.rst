==========================
JSPRPC API Documentation
==========================

Prerequisites
=============

::

    $ pip install jsonrpc 

Authentication
==============

.. code-block:: python

    import be.bootstrap
    import jsonrpc.proxy
    
    url = 'http[s]://<hostname>/app'
    
    proxy = jsonrpc.proxy.JSONRPCProxy.from_url(url)
    result = proxy.login(username='me', password='secret')
    token = result['auth_token']

API Call
========

    - Date/time format follow iso8601 standard
    - each call supports two special parameters 
        - _ctx: context (bizplace_id in most cases)
        - _token: session id

.. code-block:: python

    ctx = <bizplace_id>
    kw = dict(..)
    result = proxy.call(<apiname>,  _token=token, _ctx=ctx, **kw)#**


APIs
====

Uninvoiced usages details by members

.. code-block:: python

    # example
    start = '2013-01-31'
    result = proxy.call('usages.uninvoiced_members', res_owner_id=3, start=start, _token=token, _ctx=<ctx_id>)


Get member list

.. code-block:: python

    result = proxy.call('members.export', _token=token, _ctx=<ctx_id>)

Get member profile
includes details such as

    - contact
    - membership
    - preferences
    - account
    - profile


.. code-block:: python

    result = proxy.call('member.profile', member_id=<member_id>, _token=token, _ctx=<ctx_id>)


Get member invoicing preferences

.. code-block:: python

    result = print proxy.call('invoicepref.info', owner=<member_id>, _token=token, _ctx=<ctx_id>)
