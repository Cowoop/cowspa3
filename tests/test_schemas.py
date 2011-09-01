import commontest
import be.repository.stores as stores
import be.repository.access

commontest.setup_test_simple_env()

def test_create():
    assert bool(stores.known_stores) == True
    for store in stores.known_stores.values():
        store.setup()
    env.context.pgcursor.connection.commit()

def test_destroy():
    for store in stores.known_stores.values():
        store.destroy()
    env.context.pgcursor.connection.commit()

def test_recreate():
    for store in stores.known_stores.values():
        store.setup()
    env.context.pgcursor.connection.commit()


