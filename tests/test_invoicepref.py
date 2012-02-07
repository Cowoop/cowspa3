import commontest
import test_data
import be.repository.access as dbaccess
import be.apis.invoicepref as invoicepreflib

def setup():
    commontest.setup_test_env()
    env.context.pgcursor.connection.commit()

#def test_create_invoice_preferences():
#    assert invoicepreflib.invoicepref_collection.new(**dict(owner=1))
#    assert invoicepreflib.invoicepref_resource.get(1,'due_date') == 15

#    assert invoicepreflib.invoicepref_collection.new(**dict(owner=2))
#    assert invoicepreflib.invoicepref_resource.get(1,'due_date': 15'bcc_email') == ""

#    env.context.pgcursor.connection.commit()

def test_update_invoice_preferences():
    data = test_data.invoice_preference_data

    assert invoicepreflib.invoicepref_resource.update(test_data.bizplace_id, **data)
    assert invoicepreflib.invoicepref_resource.get(test_data.bizplace_id,'due_date') == data['due_date']

    assert invoicepreflib.invoicepref_resource.get(test_data.bizplace_id, 'taxes') == None
    assert invoicepreflib.invoicepref_resource.set(test_data.bizplace_id,'taxes', test_data.taxes)
    assert invoicepreflib.invoicepref_resource.get(test_data.bizplace_id,'taxes') == test_data.taxes

    env.context.pgcursor.connection.commit()

def test_info_invoice_preferences():
    data = invoicepreflib.invoicepref_resource.info(test_data.bizplace_id)
    for key in test_data.invoice_preference_data:
        assert test_data.invoice_preference_data[key] == data[key]


