import test_data
import commontest
import be.bootstrap
be.bootstrap.start()
import be.apps

app = be.apps.cowspa
rpc = commontest.jsonrpc

member_token = None
host_token = None

def setup():
    global member_token, host_token
    ret = rpc(app, None, None, 'login', dict(username=test_data.bizplace_member.username, password=test_data.bizplace_member.password))
    member_token = ret['result']['auth_token']
    ret = rpc(app, None, None, 'login', dict(username=test_data.bizplace_host.username, password=test_data.bizplace_host.password))
    host_token = ret['result']['auth_token']

def test_invoice_delete():
    ret = rpc(app, host_token, test_data.bizplace_id, 'invoice.list', dict(issuer=test_data.bizplace_id))
    invoice_id = ret['result'][0].id
    ret = rpc(app, member_token, test_data.bizplace_id, 'invoice.delete', dict(invoice_id=invoice_id))
    assert 'error' in ret
    ret = rpc(app, host_token, test_data.bizplace_id, 'invoice.delete', dict(invoice_id=invoice_id))
    assert 'error' not in ret
