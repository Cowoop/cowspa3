import bases.app as applib
import be.apis
import be.apis.user as userlib
import be.apis.member as memberlib
import be.apis.bizplace as bizplacelib
import be.apis.plan as planlib
import be.apis.role as rolelib
import be.apis.resource as resourcelib
import be.repository.pgdb as pgdb
import jsonrpc2
import be.wrappers as wrapperlib
import be.apis.activities as activitylib
import be.apis.invoice as invoicelib

pg_provider = pgdb.PGProvider()
pg_tr_start = lambda: pg_provider.tr_start(env.context)
pg_tr_complete = lambda: pg_provider.tr_complete(env.context)

class CSAPIExecutor(applib.APIExecutor):
    wrappers = [wrapperlib.pg_transaction]

class CowspaApp(applib.Application):
    mapper = jsonrpc2.JsonRpc()
    APIExecutor = CSAPIExecutor
    on_tr_start = [pg_tr_start]
    on_tr_complete = [pg_tr_complete]

cowspa = CowspaApp()
cowspa.connect(userlib.login)
cowspa.connect(userlib.logout)
cowspa.connect(memberlib.member_collection.new, "member.new")
cowspa.connect(bizplacelib.bizplace_collection.new, "bizplace.new")
cowspa.connect(planlib.plan_collection.new, "plan.new")
cowspa.connect(resourcelib.resource_collection.new, "resource.new")
cowspa.connect(userlib.create_superuser, "member.create_admin")
cowspa.connect(memberlib.member_collection.search, "member.search")
cowspa.connect(memberlib.member_resource.details, "member.profile")
cowspa.connect(memberlib.member_resource.contact, "member.contact")
cowspa.connect(memberlib.member_resource.update, "member.update")
cowspa.connect(activitylib.get_latest, "current.activities")
cowspa.connect(bizplacelib.bizplace_collection.list, "bizplace.list")
cowspa.connect(rolelib.get_roles, "users.bizplace.list")
cowspa.connect(planlib.plan_collection.list, "bizplace_plans.list")
cowspa.connect(planlib.plan_resource.new_subscriber, "next.tariff")
cowspa.connect(memberlib.member_resource.get_teriff_history, "teriff.history")
cowspa.connect(invoicelib.invoice_collection.search, "invoice.search")
cowspa.startup()
