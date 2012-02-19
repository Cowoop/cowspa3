import datetime
import collections
import be.repository.access as dbaccess
import be.apis.activities as activitylib
import be.apis.invoicepref as invoicepref_lib
import commonlib.shared.constants
import be.libs.signals as signals

resource_store = dbaccess.stores.resource_store
bizplace_store = dbaccess.stores.bizplace_store
resourcerelation_store = dbaccess.stores.resourcerelation_store

class CalcMode:

    quantity_based = 0
    time_based = 1
    monthly = 2

class ResourceCollection:

    def new(self, name, short_description, type, owner, default_price=None, state=None, long_description=None, calc_mode=CalcMode.monthly,
            archived=False, picture=None, accnt_code=None):
        #TODO make default_price parameter mandatory post migration
        created = datetime.datetime.now()
        if state is None:
            state = commonlib.shared.constants.resource.enabled
        else:
            state = commonlib.shared.constants.resource.to_flags(state)
        data = dict(name=name, owner=owner, created=created, short_description=short_description,
                state=state, long_description=long_description, type=type, calc_mode=calc_mode,
                archived=archived, picture=picture, accnt_code=accnt_code)
        res_id = resource_store.add(**data)

        data = dict(id=res_id, name=name, bizplace_name=dbaccess.oid2name(owner), bizplace_id=owner, user_id=env.context.user_id, created=created, type=type)
        if type == 'tariff':
            activity_id = activitylib.add('tariff_management', 'tariff_created', data, created)
        else:
            activity_id = activitylib.add('resource_management', 'resource_created', data, created)

        if default_price is not None:
            default_tariff_id = bizplace_store.get(owner, fields=['default_tariff'], hashrows=False)
            # default_tariff_id would be None when we are creating default_tariff for a new location. This is because we are adding location and there is no default_tariff yet. Now this tariff is a resource so further we need to create pricing for it. In pricing we need to specify some tariff so tariff refers itself as default_tariff.
            if default_tariff_id is None:
                default_tariff_id = res_id

            signals.send_signal('resource_created', res_id, default_tariff_id, None, default_price)
            # TODO this is not right way to send signals

        return res_id

    def new_tariff(self, name, short_description, owner, default_price, state=None, long_description=None, picture=None):
        return self.new(name, short_description, 'tariff', owner, default_price, state, long_description=long_description, calc_mode=CalcMode.monthly, picture=picture)

    def delete(self, res_id):
        """
        Deletes a resource. Only if there are no usages/members.
        """

    def list(self, owner, type=None):
        """
        type: filter by specified type
        returns list of resource info dicts
        """
        fields=['id', 'name', 'short_description', 'long_description',
                'calc_mode', 'type', 'state', 'picture', 'archived', 'accnt_code']
        resource_list = dbaccess.list_resources_and_tariffs(owner, fields, type)
        for res in resource_list:
            res['state'] = commonlib.shared.constants.resource.to_dict(res['state'])
        return resource_list

    def tariffs(self, owner):
        return self.list(owner, type='tariff')

    def available_tariffs(self, owner):
        available_state = commonlib.shared.constants.resource.to_flags( dict(enabled=True, repairs=False) )
        return resource_store.get_by(crit=dict(owner=owner, state=available_state), fields=['id', 'name'])

    def available(self, owner, calc_mode=None):
        available_state = commonlib.shared.constants.resource.to_flags( dict(enabled=True, repairs=False) )
        crit = dict(owner=owner, state=available_state)
        if calc_mode: crit['calc_mode'] = calc_mode
        return [res for res in resource_store.get_by(crit=crit, fields=['id', 'name', 'type']) if res.type != 'tariff']

    def resources(self, owner, type=None):
        """
        type: filter by specified type
        returns list of resource info dicts
        """
        fields=['id', 'name', 'short_description', 'long_description',
                'calc_mode', 'type', 'state', 'picture', 'archived', 'accnt_code']
        resource_list = dbaccess.list_resources(owner, fields, type)
        for res in resource_list:
            res['state'] = commonlib.shared.constants.resource.to_dict(res['state'])
        return resource_list


class ResourceResource:

    get_attributes = ['name', 'short_description', 'type', 'owner', 'state',
            'long_description', 'calc_mode', 'archived', 'picture', 'accnt_code', 'taxes']
    set_attributes = ['name', 'short_description', 'type', 'owner', 'state',
            'long_description', 'calc_mode', 'archived', 'picture', 'accnt_code', 'taxes']

    def info(self, res_id):
        """
        returns dict containing essential information of specified business
        """
        info_attributes = ['name', 'owner', 'short_description', 'long_description', 'state', 'id',
                'calc_mode', 'accnt_code']
        info = resource_store.get(res_id, info_attributes)
        # TODO change owner ref to name
        info['owner_id'] = info['owner']
        info['owner_name'] = dbaccess.oid2name(info['owner'])
        info['state'] = commonlib.shared.constants.resource.to_dict(info['state'])
        return info

    def update(self, res_id, **mod_data):
        """
        """
        if 'state' in mod_data: mod_data['state'] = commonlib.shared.constants.resource.to_flags(mod_data['state'])
        mod_data = dict((k,v) for k,v in mod_data.items() if k in self.set_attributes)
        resource_store.update(res_id, **mod_data)

        data = dict(user_id=env.context.user_id, res_id=res_id, attrs=', '.join(attr for attr in mod_data))
        # TODO: Add relevant event in events.py and uncomment below line
        #activity_id = activitylib.add('ResourceManagement', 'ResourceUpdated', env.context.user_id, data)

    def get(self, res_id, attrname):
        if not attrname in self.get_attributes: return
        value = resource_store.get(res_id, fields=[attrname], hashrows=False)
        return value if attrname != 'state' else commonlib.shared.constants.resource.to_dict(value)

    def set(self, res_id, attrname, v):
        if not attrname in self.set_attributes: return
        v = commonlib.shared.constants.resource.to_flags(v) if attrname == 'state' else v
        self.update(res_id, **{attrname: v})

    def set_relations(self, res_id, relations):
        """
        relations: list of tuples containing other resource id and relation (integer)
        eg. Resource 12 contains resources 13, 14 and suggests 15.
        >>> set_relations(12, [(True, 13), (True, 14), (False, 15)])
        """
        relation_dicts = dict((resb_id, relation) for relation, resb_id in relations)
        existing_relations = dict(resourcerelation_store.get_by(crit={'resourceA':res_id}, fields=['relation', 'resourceB'], hashrows=False))
        to_update = set(relation_dicts.keys()).intersection(existing_relations.keys())
        to_add = set(relation_dicts.keys()).difference(to_update)
        for resB_id in to_add:
            resourcerelation_store.add(resourceA=res_id, relation=relation_dicts[resB_id], resourceB=resB_id)
        for resB_id in to_update:
            resourcerelation_store.update_by(resourceA=res_id, relation=relation_dicts[resB_id], resourceB=resB_id)
        return resourcerelation_store.get_by(crit={'resourceA':res_id})

    def get_relations(self, res_id):
        """
        returns dict keyed by relation and resource_id, resource_name as values
        """
        relations = resourcerelation_store.get_by(crit={'resourceA':res_id}, fields=['relation', 'resourceB'], hashrows=False)
        other_res_ids = tuple(rel[1] for rel in relations)
        other_resources = dict(resource_store.get_many(other_res_ids, fields=['id', 'name'], hashrows=False))
        d = collections.defaultdict(list)
        for relation, other_res_id in relations:
            d[relation].append(dict(id=other_res_id, name=other_resources[other_res_id]))
        return d

    def get_taxinfo(self, res_id, resource_owner=None):
        """
        if resource level taxes has precedance over location level taxes
        returns tax information dict
            eg. {tax_included: True/False, taxes: {label: value, ..}
        if res_id is 0 ie custom resource then return location level taxes
        """
        owner = resource_owner if resource_owner else self.get(res_id, 'owner')
        taxinfo = invoicepref_lib.invoicepref_resource.get_taxinfo(owner)
        resource_taxes = self.get(res_id, 'taxes') if res_id != 0 else None
        if resource_taxes != None: taxinfo['taxes'] = resource_taxes
        return taxinfo

resource_resource = ResourceResource()
resource_collection = ResourceCollection()
