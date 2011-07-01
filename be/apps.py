import bases.app as applib
import be.apis
import be.apis.member as memberlib

mapper = applib.Mapper()
mapper.connect_collection('members', memberlib.member_collection)
mapper.connect_resource('members/<int:member_id>', memberlib.member_resource)

locator = mapper.build()

app = applib.Dispatcher(locator, )
