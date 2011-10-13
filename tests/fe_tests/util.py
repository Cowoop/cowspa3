from windmill.authoring import WindmillTestClient
# from windmill.authoring import setup_module, teardown_module

def logged_in_client(test_url='http://localhost:5001/login', username=u'shon', passwd=u'x', client=None):

    if client is None:
        client = WindmillTestClient(__name__)
    
    client.open(url=test_url)
    client.click(id=u'username')
    client.type(text=username, id=u'username')
    # client.type(text=functest.registry['username'], id=u'username')
    client.click(id=u'password')
    client.type(text=passwd, id=u'password')
    # client.type(text=functest.registry['passwd'], id=u'password')
    client.click(id=u'login-btn')

    return client


def logout(client):
    client.click(link=u'Logout')
    client.waits.forPageLoad(timeout=u'20000')
    client.asserts.assertNode(id=u'login-btn')
    client.asserts.assertText(validator=u'Log In', id=u'login-btn')
