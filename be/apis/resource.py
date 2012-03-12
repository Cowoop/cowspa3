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

    def new(self, name, short_description, type, owner, default_price=None, enabled=True, calendar=False, host_only=False, long_description=None, calc_mode=CalcMode.monthly, archived=False, picture=None, accnt_code=None):
        #TODO make default_price parameter mandatory post migration
        created = datetime.datetime.now()
        data = dict(name=name, owner=owner, created=created, short_description=short_description, enabled=enabled, calendar=calendar, host_only=host_only, long_description=long_description, type=type, calc_mode=calc_mode, archived=archived, picture=picture, accnt_code=accnt_code)
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

    def new_tariff(self, name, short_description, owner, default_price, enabled=True, long_description=None, picture=None):
        return self.new(name, short_description, 'tariff', owner, default_price, enabled, long_description=long_description, calc_mode=CalcMode.monthly, picture=picture)

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
                'calc_mode', 'type', 'enabled', 'host_only', 'picture', 'archived', 'accnt_code']
        resource_list = dbaccess.list_resources_and_tariffs(owner, fields, type)
        return resource_list

    def tariffs(self, owner):
        return self.list(owner, type='tariff')

    def available_tariffs(self, owner):
        return resource_store.get_by(crit=dict(owner=owner, enabled=True), fields=['id', 'name'])

    def available(self, owner, calc_mode=None, role='member'):
        crit = dict(owner=owner, enabled=True)
        if calc_mode: crit['calc_mode'] = calc_mode
        fields = ['id', 'name', 'type', 'calc_mode']
        return [res for res in resource_store.get_by(crit=crit, fields=fields) if res.type != 'tariff']

    def available_for_booking(self, owner, for_member):
        crit = dict(owner=owner, enabled=True, archived=False, calendar=True, calc_mode=CalcMode.time_based)
        fields = ['id', 'name', 'type', 'calc_mode']
        resources = [res for res in resource_store.get_by(crit=crit, fields=fields) if res.type != 'tariff']
        pricings = dbaccess.get_pricings_for_member(owner, for_member)
        for resource in resources:
            relations = resource_resource.get_relations(resource.id)
            resource['contained'] = relations[True]
            resource['suggested'] = relations[False]
            resource['price'] = pricings[resource.id].price
            for c_resource in resource['contained']:
                c_resource['price'] = pricings[c_resource.id].price
            for s_resource in resource['suggested']:
                s_resource['price'] = pricings[s_resource.id].price
        return resources

    def bookable(self, owner):
        resources = self.available(owner)
        contained_resource_ids = [row[0] for row in resourcerelation_store.get_by(dict(owner=owner, relation=True), fields=['resourceB'], hashrows=False)]
        return [res for res in resources if res.id not in contained_resource_ids]

    def resources(self, owner, type=None):
        """
        type: filter by specified type
        returns list of resource info dicts
        """
        fields=['id', 'name', 'short_description', 'long_description',
                'calc_mode', 'type', 'enabled', 'host_only', 'picture', 'archived', 'accnt_code']
        resource_list = dbaccess.list_resources(owner, fields, type)
        return resource_list


class ResourceResource:

    get_attributes = ['name', 'short_description', 'type', 'owner', 'enabled', 'archived', 'host_only', 'calendar',
            'long_description', 'calc_mode', 'archived', 'picture', 'accnt_code', 'taxes']
    set_attributes = ['name', 'short_description', 'type', 'owner', 'enabled', 'archived', 'host_only', 'calendar',
            'long_description', 'calc_mode', 'archived', 'picture', 'accnt_code', 'taxes']

    def info(self, res_id):
        """
        returns dict containing essential information of specified business
        """
        info_attributes = ['name', 'owner', 'short_description', 'long_description', 'enabled', 'id', 'type', 'host_only',
                'archived', 'calc_mode', 'accnt_code']
        info = resource_store.get(res_id, info_attributes)
        # TODO change owner ref to name
        info['owner_id'] = info['owner']
        info['owner_name'] = dbaccess.oid2name(info['owner'])
        return info

    def update(self, res_id, **mod_data):
        """
        """
        mod_data = dict((k,v) for k,v in mod_data.items() if k in self.set_attributes)
        resource_store.update(res_id, **mod_data)

        data = dict(user_id=env.context.user_id, res_id=res_id, attrs=', '.join(attr for attr in mod_data))
        # TODO: Add relevant event in events.py and uncomment below line
        #activity_id = activitylib.add('ResourceManagement', 'ResourceUpdated', env.context.user_id, data)

    def get(self, res_id, attrname):
        if not attrname in self.get_attributes: return
        return resource_store.get(res_id, fields=[attrname], hashrows=False)

    def set(self, res_id, attrname, v):
        if not attrname in self.set_attributes: return
        self.update(res_id, **{attrname: v})

    def set_relations(self, res_id, relations):
        """
        relations: list of tuples containing other resource id and relation (integer)
        eg. Resource 12 contains resources 13, 14 and suggests 15.
        >>> set_relations(12, [(True, 13), (True, 14), (False, 15)])
        """
        owner = resource_store.get(res_id, ['owner'])
        relation_dicts = dict((resb_id, relation) for relation, resb_id in relations)
        existing_relations = dict(resourcerelation_store.get_by(crit={'resourceA':res_id}, fields=['resourceB', 'relation'], hashrows=False))
        to_update = set(relation_dicts.keys()).intersection(existing_relations.keys())
        to_add = set(relation_dicts.keys()).difference(to_update)
        for resB_id in to_add:
            resourcerelation_store.add(owner=owner, resourceA=res_id, relation=relation_dicts[resB_id], resourceB=resB_id)
        for resB_id in to_update:
            resourcerelation_store.update_by(crit=dict(resourceA=res_id, resourceB=resB_id), relation=relation_dicts[resB_id])
        return resourcerelation_store.get_by(crit={'resourceA':res_id})

    def get_relations(self, res_id):
        """
        returns dict keyed by relation and list of resource_id, resource_name as values
        """
        relations = resourcerelation_store.get_by(crit={'resourceA':res_id}, fields=['relation', 'resourceB'], hashrows=False)
        other_res_ids = tuple(rel[1] for rel in relations)
        other_resources = dict((res.id, res) for res in resource_store.get_many(other_res_ids, fields=['id', 'name', 'calc_mode']))
        d = collections.defaultdict(list)
        for relation, other_res_id in relations:
            d[relation].append(other_resources[other_res_id])
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
