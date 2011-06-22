import commontest
import psycopg2.pool
import bases.persistence as persistence

cursor_getter = commontest.setup_test_cursor()

class UserStore(persistence.PGStore):
    cursor_getter = cursor_getter
    table_name = 'account1'
    create_sql = """
    id SERIAL NOT NULL UNIQUE,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    enabled boolean default true NOT NULL
    """

test_data = dict(username='test', password='x', enabled=True)

user_store = None

def setup():
    global user_store
    user_store = UserStore()
    user_store.destroy()
    user_store.setup()

def teardown():
    user_store.destroy()

def test_resetup():
    user_store = UserStore()
    user_store.setup()

def test_add():
    user_id = user_store.add(**test_data)
    assert user_id == 1

def test_get():
    user = user_store.get(1)
    assert user.id == 1

def test_get2():
    user1 = user_store.get(1)
    user2 = user_store.get_one_by(crit={'id':1})
    user3 = user_store.get_by(crit={'id':1})
    assert (user1==user2==user3[0]) == True

def test_get3():
    user = user_store.get_one_by(crit=test_data)
    assert bool(user)

def test_all():
    users = user_store.get_all()
    count = user_store.count()
    assert len(users) == count

def test_many():
    user_ids = user_store.get_all(fields=['id'], hashrows=False)
    user_store.get_many(oids=user_ids)

def test_remove():
    crit = dict(id=1)
    user_store.remove_by(crit=crit)
    user = user_store.get_one_by_safe(crit)
    assert user == None
