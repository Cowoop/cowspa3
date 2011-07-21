import datetime
import be.repository.access as dbaccess

resource_store = dbaccess.stores.resource_store

class ResourceCollection:

    def new(self, name, owner, short_description, long_description=None):
        created = datetime.datetime.now()
        data = dict(name=name, owner=owner, created=created, short_description=short_description, long_description=long_description)
        res_id = resource_store.add(**data)

        return res_id

    def list(self, owner):
        """
        returns list of resource info dicts
        """

class ResourceResource:

    get_attributes = ['name', 'short_description', 'long_description']
    set_attributes = ['name', 'short_description', 'long_description']

    def info(self, res_id):
        """
        returns dict containing essential information of specified business
        """
        info_attributes = ['name', 'owner', 'short_description']
        info = resource_store.get(res_id, info_attributes)
        print(info)
        # TODO change owner ref to name
        info['owner_id'] = info['owner']
        info['owner_name'] = dbaccess.ref2name(info['owner'])
        return info

    def update(self, res_id, **mod_data):
        """
        """
        mod_data = dict((k,v) for k,v in mod_data.items() if k in self.set_attributes)
        resource_store.update(res_id, **mod_data)

resource_resource = ResourceResource()
resource_collection = ResourceCollection()
