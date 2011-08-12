import bases.app as applib
import be.apis
import be.apis.user as userlib
import be.apis.member as memberlib
import be.apis.bizplace as bizplacelib
import be.apis.plan as planlib
import be.apis.resource as resourcelib
import be.repository.pgdb as pgdb
import jsonrpc2
import be.wrappers as wrapperlib

pg_provider = pgdb.PGProvider()

class CSAPIExecutor(applib.APIExecutor):
    wrappers = [wrapperlib.pg_transaction]

class CowspaApp(applib.Application):
    mapper = jsonrpc2.JsonRpc()
    APIExecutor = CSAPIExecutor

cowspa = CowspaApp()
cowspa.connect(userlib.login)
cowspa.connect(memberlib.member_collection.new, "member.new")
cowspa.connect(bizplacelib.bizplace_collection.new, "bizplace.new")
cowspa.connect(planlib.plan_collection.new, "plan.new")
cowspa.connect(resourcelib.resource_collection.new, "resource.new")
cowspa.connect(userlib.create_superuser, "super.create")
cowspa.startup()
