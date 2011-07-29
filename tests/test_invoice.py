import commontest
import datetime
import be.repository.access as dbaccess
import be.apis.invoice as invoicelib
import test_usage
import test_member

invoice_data = dict(member=1, usages=[1,3])
more_invoice_data = [
    dict(member=2, usages=[1]),
    dict(member=3, usages=[3])
    ]


def setup():
    commontest.setup_test_env()
    env.context.pgcursor.connection.commit()
    test_usage.test_add_usage()
    test_usage.test_add_more_usage()
    test_member.test_create_member()

def teardown():
    commontest.destroy_test_env()
    env.context.pgcursor.connection.commit()

def test_add_invoice():
    invoice_id = invoicelib.invoice_collection.new(**invoice_data)
    env.context.pgcursor.connection.commit()
    assert invoice_id == 1
    assert dbaccess.usage_store.get(3, ['invoice']) == invoice_id

def test_send():
    invoicelib.invoice_resource.send(1)

def test_update_invoice():
    mod_data = dict(usages=[2,4], member=2)
    assert invoicelib.invoice_resource.update(1, mod_data)
    assert dbaccess.invoice_store.get(1, ['member']) == mod_data['member']

def test_add_more_invoice():
    for data in more_invoice_data:
        invoice_id = invoicelib.invoice_collection.new(**data)
    env.context.pgcursor.connection.commit()
    
def tests_delete_invoice():
    assert invoicelib.invoice_collection.delete(1)
    assert dbaccess.usage_store.get(2, ['invoice']) == None
    
