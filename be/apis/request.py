import datetime
import commonlib.helpers
import be.errors as errors
import be.repository.access as dbaccess
import be.apis.role as rolelib

request_store = dbaccess.stores.request_store
requestpermission_store = dbaccess.stores.requestpermission_store

states = commonlib.helpers.odict(
    pending = 0,
    approved = 1,
    rejected = 2,
    ignored = 3)

class RequestHelper(object):
    label = "Base Request"
    def __init__(self, requestor_id, api, params):
        self.requestor_id = requestor_id
        self.api = api
        self.params = params
    def to_html(self):
        requestor_name = dbaccess.oid2name(self.requestor_id)
        requestor = requestor_name + " (%s) " % self.requestor_id
        msg_data = dict(label=self.label, api=self.api, params=self.params, requestor=requestor)
        return "%(label)s by %(member)s for %(api)s with data %(params)s" % msg_data
    def approver_perms(self):
        """
        returns a list of approver contexted permission strings
        eg. ["3:approve_membership", "0:admin"]
        """
        raise NotImplemented

class Membership(RequestHelper):
    label = "Membership request"
    def to_html(self):
        label = self.label
        requestor_name = dbaccess.oid2name(self.requestor_id)
        requestor = requestor_name + " [%s]" % self.requestor_id
        tariff_name = dbaccess.stores.plan_store.get(self.params['plan_id']).name
        return '%(label)s by "%(requestor)s" for tariff "%(tariff_name)s"' % locals()
    def approver_perms(self):
        bizplace_id = dbaccess.stores.plan_store.get(self.params['plan_id']).bizplace
        return [str(bizplace_id) + dbaccess.ctxsep + 'approve_membership']

class NewTeamMember(RequestHelper):
    label = "Join team request"
    def to_html(self):
        label = self.label
        requestor_name = dbaccess.oid2name(self.requestor_name)
        requestor = requestor_name + " (%s) " % requestor_id
        bizplace = dbaccess.oid2name(bizplace_id)
        return '"%(label)s by %(requestor)s for %(bizplace)s"' % locals()
    def approver_perm(self):
        return [(self.params['bizplace'], 'manage_team')]

req_helpers = dict(
    membership = Membership,
    newteammember = NewTeamMember)

################## APIs #################

def new(name, requestor_id, api, params):
    """
    return True/False
    """
    created = datetime.datetime.now()
    req_helper = req_helpers[name](requestor_id, api, params)
    approver_perms = req_helper.approver_perms()
    req_id = request_store.add(name=name, requestor_id=requestor_id, api=api, params=params, created=created, state=states.pending)
    requestpermission_store.add_many([dict(request=req_id, permission=permission) for permission in approver_perms])
    return req_id

def info(req_id):
    return request_store.get(req_id)

def act(req_id, action_code, note=None):
    """
    """
    if action_code not in states.values():
        raise errors.ErrorWithHint('Unrecognized approval option')

    import be.apps # to avoid circular imports
    app = be.apps.cowspa
    req = request_store.get(req_id)
    if action_code == states.approved:
        app.mapper[req.api](**req.params)
    request_store.update(req.id, state=action_code, acted=datetime.datetime.now())
    # TODO processed requests should be archived/removed after a while

def add_messages(reqs):
    requests_list = []
    for req in reqs:
        req_helper = req_helpers[req.name](req.requestor_id, req.api, req.params)
        req['msg'] = req_helper.to_html()
        requests_list.append(req)
    return requests_list

def made(requestor_id, limit=10):
    """
    return list of dicts
    {id=id, created=created, state=state, msg=msg, approver=approver, acted=acted}
    """
    return add_messages(request_store.get_by(dict(requestor_id=requestor_id, state=states.pending), limit=limit))

def in_queue(for_id, only_pending=True):
    """
    return list of dicts
    {id=id, created=created, state=state, msg=msg, requestor=requestor}
    """
    perms = rolelib.get_permissions(for_id)
    requests_list = []
    return add_messages(dbaccess.find_requests_for_approval(perms))
