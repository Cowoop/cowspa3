import datetime
import collections
import be.repository.access as dbaccess
import be.apis.activities as activitylib
import be.apis.pricing as pricinglib
import commonlib.shared.constants

resource_store = dbaccess.stores.resource_store
bizplace_store = dbaccess.stores.bizplace_store
resourcerelation_store = dbaccess.stores.resourcerelation_store

class ResourceCollection:

    def new(self, name, short_description, type, owner, default_price, state=None, long_description=None, time_based=False, archived=False, picture=None):
        created = datetime.datetime.now()
        if state is None:
            state = 2 ** commonlib.shared.constants.resource.enabled
        else:
            state = commonlib.shared.constants.resource.to_flags(state)
        data = dict(name=name, owner=owner, created=created, short_description=short_description, state=state, long_description=long_description, type=type, time_based=time_based, archived=archived, picture=picture)
        res_id = resource_store.add(**data)

        data = dict(id=res_id, name=name, bizplace_name=dbaccess.oid2name(owner), bizplace_id=owner, user_id=env.context.user_id, created=created, type=type)
        if type == 'tariff':
            activity_id = activitylib.add('tariff_management', 'tariff_created', data, created)
        else:
            activity_id = activitylib.add('resource_management', 'resource_created', data, created)

        default_tariff_id = bizplace_store.get(owner, fields=['default_tariff'], hashrows=False)
        # default_tariff_id would be None when we are creating default_tariff for a new location. This is because we are adding location and there is no default_tariff yet. Now this tariff is a resource so further we need to create pricing for it. In pricing we need to specify some tariff so tariff refers itself as default_tariff.
        if default_tariff_id is None:
            default_tariff_id = res_id
        pricinglib.pricings.new(res_id, default_tariff_id, created.date().isoformat(), default_price)

        return res_id

    def new_tariff(self, name, short_description, owner, default_price, state=None, long_description=None, picture=None):
        return self.new(name, short_description, 'tariff', owner, default_price, state, long_description=long_description, time_based=True, picture=picture)

    def delete(self, res_id):
        """
        Deletes a resource. Only if there are no usages/members.
        """

    def list(self, owner, type=None):
        """
        type: filter by specified type
        returns list of resource info dicts
        """
        fields=['id', 'name', 'short_description', 'long_description', 'time_based', 'type', 'state', 'picture', 'archived']
        resource_list = dbaccess.list_resources(owner, fields, type)
        for res in resource_list:
            res['state'] = commonlib.shared.constants.resource.to_dict(res['state'])
        return resource_list

class ResourceResource:

    get_attributes = ['name', 'short_description', 'type', 'owner', 'state', 'long_description', 'time_based', 'archived', 'picture']
    set_attributes = ['name', 'short_description', 'type', 'owner', 'state', 'long_description', 'time_based', 'archived', 'picture']

    def info(self, res_id):
        """
        returns dict containing essential information of specified business
        """
        info_attributes = ['name', 'owner', 'short_description', 'state', 'id']
        info = resource_store.get(res_id, info_attributes)
        # TODO change owner ref to name
        info['owner_id'] = info['owner']
        info['owner_name'] = dbaccess.oid2name(info['owner'])
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

resource_resource = ResourceResource()
resource_collection = ResourceCollection()
