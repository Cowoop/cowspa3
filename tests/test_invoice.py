import commontest
import test_data

import datetime
import be.repository.access as dbaccess
import be.apis.invoice as invoicelib
import test_usage
import test_member

# dependencies member usage

def test_add_invoice():
    invoice_id = invoicelib.invoice_collection.new(**test_data.invoice_data)
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
    for data in test_data.more_invoice_data:
        invoice_id = invoicelib.invoice_collection.new(**data)
    env.context.pgcursor.connection.commit()

def tests_delete_invoice():
    assert invoicelib.invoice_collection.delete(1)
    assert dbaccess.usage_store.get(2, ['invoice']) == None

