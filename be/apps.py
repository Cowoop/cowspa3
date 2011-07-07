import bases.app as applib
import be.apis
import be.apis.member as memberlib
import be.repository.pgdb as pgdb

mapper = applib.Mapper()
mapper.connect_collection('members', memberlib.member_collection)
mapper.connect_resource('members/<int:member_id>', memberlib.member_resource)

locator = mapper.build()
pg_provider = pgdb.PGProvider()

app = applib.Application()
app.root = applib.Dispatcher(locator, pg_provider)
