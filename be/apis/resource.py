import datetime
import collections
import be.repository.access as dbaccess
import commonlib.shared.constants as constants

resource_store = dbaccess.stores.resource_store
resourcerelation_store = dbaccess.stores.resourcerelation_store

class ResourceCollection:

    def new(self, name, short_description, type, owner=1, long_description=None, time_based=True, quantity_unit=None):
        created = datetime.datetime.now()
        data = dict(name=name, owner=owner, created=created, short_description=short_description, long_description=long_description, type=type, time_based=time_based, quantity_unit=quantity_unit)
        res_id = resource_store.add(**data)

        return res_id

    def list(self, owner):
        """
        returns list of resource info dicts
        """
        return resource_store.get_by(owner=owner, fields=['id', 'name', 'short_description'])

class ResourceResource:

    get_attributes = ['name', 'short_description', 'long_description']
    set_attributes = ['name', 'short_description', 'long_description']

    def info(self, res_id):
        """
        returns dict containing essential information of specified business
        """
        info_attributes = ['name', 'owner', 'short_description']
        info = resource_store.get(res_id, info_attributes)
        # TODO change owner ref to name
        info['owner_id'] = info['owner']
        info['owner_name'] = dbaccess.ref2name(info['owner'])
        return info

    def update(self, res_id, **mod_data):
        """
        """
        mod_data = dict((k,v) for k,v in mod_data.items() if k in self.set_attributes)
        resource_store.update(res_id, **mod_data)

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
        >>> set_relations(12, [('contains', 13), ('contains', 14), ('suggests', 15)])
        """
        relations = [(resb_id, getattr(constants.resource_relations, relation)) for relation, resb_id in relations]
        relation_dicts = dict(relations)
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
            d[constants.resource_relations.rev(relation)].append(dict(id=other_res_id, name=other_resources[other_res_id]))
        return d

resource_resource = ResourceResource()
resource_collection = ResourceCollection()
