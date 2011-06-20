import commontest
import be.repository.stores as stores

commontest.setup_test_simple_env()

def test_create():
    import be.repository.access
    assert bool(stores.known_stores) == True
    env.context.pgcursor.connection.commit()

def test_destroy():
    for store in stores.known_stores.values():
        store.destroy()
    env.context.pgcursor.connection.commit()
