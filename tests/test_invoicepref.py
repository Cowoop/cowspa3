import commontest
import test_data
import be.repository.access as dbaccess
import be.apis.invoicepref as invoicepreflib

def setup():
    commontest.setup_test_env()
    env.context.pgcursor.connection.commit()

def test_create_invoice_preferences():
    assert invoicepreflib.invoicepref_collection.new(**dict(owner=dbaccess.stores.bizplace_store.ref(1)))
    assert invoicepreflib.invoicepref_resource.get(1,'due_date') == 15
    
    assert invoicepreflib.invoicepref_collection.new(**dict(owner=dbaccess.stores.bizplace_store.ref(2)))
    assert invoicepreflib.invoicepref_resource.get(1,'bcc_email') == ""
    
    env.context.pgcursor.connection.commit()

def test_update_invoice_preferences():
    data = test_data.invoice_preference_data
    assert invoicepreflib.invoicepref_resource.update(1, **data[0])
    assert invoicepreflib.invoicepref_resource.get(1,'due_date') == data[0]['due_date']
    
    assert invoicepreflib.invoicepref_resource.update(2, **data[1])
    assert invoicepreflib.invoicepref_resource.get(2,'bcc_email') == data[1]['bcc_email']
    
    assert invoicepreflib.invoicepref_resource.set(1,'bcc_email','gaurav.hub@gmail.com') 
    assert invoicepreflib.invoicepref_resource.get(1,'bcc_email') != data[1]['bcc_email']
    assert invoicepreflib.invoicepref_resource.get(1,'bcc_email') == "gaurav.hub@gmail.com"
    
def test_info_invoice_preferences():
    data = invoicepreflib.invoicepref_resource.info(2)
    for key in data:
        assert test_data.invoice_preference_data[1][key] == data[key]
        
