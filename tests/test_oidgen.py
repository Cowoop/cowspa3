import commontest
import be.repository.access as dbaccess

def setup():
    commontest.setup_test_env()
    env.context.pgcursor.connection.commit()

def test_oid_generation():
    
    oid = dbaccess.OidGenerator.next("Member")
    assert isinstance(oid, (long, int))
    assert dbaccess.OidGenerator.get_otype(oid) == "Member"
    env.context.pgcursor.connection.commit()
    
def test_more():
    otypes = ["Biz", "Bizplace", "Member"]
    for otype in otypes:
        oid = dbaccess.OidGenerator.next(otype)
        assert isinstance(oid, (long, int))
        assert dbaccess.OidGenerator.get_otype(oid) == otype
    env.context.pgcursor.connection.commit()
