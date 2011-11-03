import bases.app as applib
import be.apis
import be.apis.system as systemlib
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
import be.apis.invoicepref as invoicepreflib
import be.apis.registration as registrationlib
import be.apis.billingpref as billingpreflib

pg_provider = pgdb.PGProvider(env.config.threaded)
pg_tr_start = lambda: pg_provider.tr_start(env.context)
pg_tr_complete = lambda: pg_provider.tr_complete(env.context)
pg_tr_abort = lambda: pg_provider.tr_abort(env.context)

class CSAPIExecutor(applib.APIExecutor):
    wrappers = [wrapperlib.pg_transaction]

class CowspaApp(applib.Application):
    mapper = jsonrpc2.JsonRpc()
    APIExecutor = CSAPIExecutor
    on_tr_start = [pg_tr_start]
    on_tr_complete = [pg_tr_complete]
    on_tr_abort = [pg_tr_abort]

cowspa = CowspaApp()
cowspa.connect(systemlib.setup)
cowspa.connect(userlib.login)
cowspa.connect(userlib.logout)
cowspa.connect(registrationlib.new, "registration.new")
cowspa.connect(registrationlib.activate, "registration.activate")
cowspa.connect(memberlib.member_collection.new, "member.new")
cowspa.connect(bizplacelib.bizplace_collection.new, "bizplace.new")
cowspa.connect(planlib.plan_collection.new, "plan.new")
cowspa.connect(resourcelib.resource_collection.new, "resource.new")
cowspa.connect(resourcelib.resource_collection.list, "resource.list")
cowspa.connect(resourcelib.resource_resource.update, "resource.update")
cowspa.connect(memberlib.member_collection.search, "members.search")
cowspa.connect(memberlib.member_resource.details, "member.profile")
cowspa.connect(memberlib.member_resource.contact, "member.contact")
cowspa.connect(memberlib.member_resource.update, "member.update")
cowspa.connect(activitylib.get_latest, "current.activities")
cowspa.connect(bizplacelib.bizplace_collection.list, "bizplace.list")
cowspa.connect(rolelib.get_roles, "users.bizplace.list")
cowspa.connect(planlib.plan_collection.list, "bizplace_plans.list")
cowspa.connect(planlib.plan_resource.new_subscriber, "plan.new_subscriber")
cowspa.connect(memberlib.member_resource.get_teriff_history, "teriff.history")
cowspa.connect(invoicelib.invoice_collection.new, "invoice.new")
cowspa.connect(invoicelib.invoice_collection.search, "invoices.search")
cowspa.connect(invoicelib.invoice_resource.send, "invoice.send")
cowspa.connect(invoicelib.invoice_collection.list, "invoice.history")
cowspa.connect(invoicepreflib.invoicepref_resource.info, "invoicepref.info")
cowspa.connect(invoicepreflib.invoicepref_resource.update, "invoicepref.update")
cowspa.connect(planlib.plan_resource.remove_subscriber, "subscription.remove")
cowspa.connect(planlib.plan_resource.change_subscription, "subscription.change")
cowspa.connect(billingpreflib.billingpref_resource.info, "billingpref.info")
cowspa.connect(billingpreflib.billingpref_resource.update, "billingpref.update")
cowspa.connect(billingpreflib.billingpref_resource.get_details, "billingpref.details")
cowspa.startup()
