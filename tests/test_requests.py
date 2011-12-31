import commontest
import test_data
import datetime
import be.apis.request as requestlib

def setup():
    commontest.setup_test_env()
    env.context.pgcursor.connection.commit()
    commontest.setup_system_context()

def test_new_req():
    requestor_id = test_data.member_id
    request_name = 'membership'
    request_api = 'memberships.new'
    request_params = dict(tariff_id=test_data.plan_id, member_id=test_data.more_member_ids[0], starts=datetime.date(2011, 4, 1).isoformat(), ends=datetime.date(2011, 4, 30).isoformat())
    req_id = requestlib.new(request_name, requestor_id, request_api, request_params)
    test_data.request_id = req_id
    env.context.pgcursor.connection.commit()
    assert requestlib.info(req_id).params == request_params

def test_requests_made():
    requestor_id = test_data.member_id
    reqs = requestlib.made(requestor_id)
    req_ids = [req.id for req in reqs]
    assert test_data.request_id in req_ids

def test_list():
    reqs = requestlib.in_queue(test_data.member_id)
    req_ids = [req.id for req in reqs]
    assert test_data.request_id in req_ids

def test_act_on_req():
    req_id = test_data.request_id
    requestlib.act(req_id, requestlib.states.approved)
    env.context.pgcursor.connection.commit()
    assert requestlib.info(req_id).state == requestlib.states.approved
