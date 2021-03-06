import bases.app as applib
import be.apis
import be.apis.system as systemlib
import be.apis.user as userlib
import be.apis.member as memberlib
import be.apis.bizplace as bizplacelib
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
import be.apis.membership as membershiplib
import be.apis.pricing as pricinglib
import be.apis.usage as usagelib
import be.apis.messagecust as messagecustlib

pg_provider = pgdb.PGProvider(env.config.threaded)
pg_tr_start = lambda: pg_provider.tr_start(env.context)
pg_tr_complete = lambda: pg_provider.tr_complete(env.context)
pg_tr_abort = lambda: pg_provider.tr_abort(env.context)

class CSAPIExecutor(applib.APIExecutor):
    wrappers = [wrapperlib.pg_transaction, wrapperlib.access_check]

class CowspaApp(applib.Application):
    mapper = jsonrpc2.JsonRpc()
    APIExecutor = CSAPIExecutor
    on_tr_start = [pg_tr_start]
    on_tr_complete = [pg_tr_complete]
    on_tr_abort = [pg_tr_abort]

cowspa = CowspaApp()
cowspa.context_setter = userlib.set_context_by_session # ugly
cowspa.connect(userlib.login)
cowspa.connect(userlib.logout)
#cowspa.connect(registrationlib.new, "registration.new")
cowspa.connect(registrationlib.invite, "registration.invite")
cowspa.connect(registrationlib.activate, "registration.activate")
cowspa.connect(memberlib.member_collection.new, "member.new")
cowspa.connect(bizplacelib.bizplace_collection.new, "bizplace.new")
cowspa.connect(resourcelib.resource_collection.new, "resource.new")
cowspa.connect(resourcelib.resource_collection.list, "resource.list")
cowspa.connect(resourcelib.resource_collection.available, "resources.available")
cowspa.connect(resourcelib.resource_collection.available_for_booking, "resources.available_for_booking")
cowspa.connect(resourcelib.resource_collection.bookable, "resources.bookable")
cowspa.connect(resourcelib.resource_collection.tariffs, "tariffs.list")
cowspa.connect(resourcelib.resource_resource.update, "resource.update")
cowspa.connect(resourcelib.resource_resource.info, "resource.info")
cowspa.connect(resourcelib.resource_resource.get, "resource.get")
cowspa.connect(resourcelib.resource_resource.get_relations, "resource.get_relations")
cowspa.connect(resourcelib.resource_resource.set_relations, "resource.set_relations")
cowspa.connect(memberlib.member_collection.search, "members.search")
cowspa.connect(memberlib.member_collection.export, "members.export")
cowspa.connect(memberlib.member_resource.info, "member.info")
cowspa.connect(memberlib.member_resource.details, "member.profile")
cowspa.connect(memberlib.member_resource.contact, "member.contact")
cowspa.connect(memberlib.member_resource.update, "member.update")
cowspa.connect(memberlib.member_resource.get, "member.get")
cowspa.connect(activitylib.get_latest, "activities.recent")
cowspa.connect(bizplacelib.bizplace_collection.list, "bizplace.list")
cowspa.connect(bizplacelib.bizplace_collection.all, "bizplace.all")
cowspa.connect(rolelib.get_roles, "roles.list")
cowspa.connect(rolelib.get_roles_in_context, "roles.context.list")
cowspa.connect(rolelib.get_team, "roles.team")
cowspa.connect(rolelib.new_roles, "roles.add")
cowspa.connect(rolelib.remove_roles, "roles.remove")
cowspa.connect(bizplacelib.bizplace_resource.info, "bizplace.info")
cowspa.connect(bizplacelib.bizplace_resource.update, "bizplace.update")
cowspa.connect(bizplacelib.bizplace_resource.currency, "bizplace.currency")
cowspa.connect(invoicelib.invoice_collection.new, "invoice.new")
cowspa.connect(invoicelib.invoice_collection.m_new, "invoice.m_new")
cowspa.connect(invoicelib.invoice_collection.delete, "invoice.delete")
cowspa.connect(invoicelib.invoice_collection.search, "invoices.search")
cowspa.connect(invoicelib.invoice_resource.update, "invoice.update")
cowspa.connect(invoicelib.invoice_resource.send, "invoice.send")
cowspa.connect(invoicelib.invoice_resource.get, "invoice.get")
cowspa.connect(invoicelib.invoice_collection.list, "invoice.list")
cowspa.connect(invoicelib.invoice_collection.unsent, "invoices.unsent")
cowspa.connect(invoicelib.invoice_collection.generate, "invoices.generate")
cowspa.connect(invoicelib.invoice_collection.by_member, "invoice.by_member")
cowspa.connect(invoicepreflib.invoicepref_resource.info, "invoicepref.info")
cowspa.connect(invoicepreflib.invoicepref_resource.update, "invoicepref.update")
cowspa.connect(invoicepreflib.invoicepref_resource.get_taxinfo, "invoicepref.taxinfo")
cowspa.connect(membershiplib.memberships, "memberships")
cowspa.connect(membershiplib.membership, "membership")
cowspa.connect(pricinglib.pricings, "pricings")
cowspa.connect(pricinglib.pricing, "pricing")
cowspa.connect(pricinglib.calculate_cost, "pricing.calculate_cost")
cowspa.connect(messagecustlib.new, "messagecust.new")
cowspa.connect(messagecustlib.get, "messagecust.get")
cowspa.connect(messagecustlib.update, "messagecust.update")
cowspa.connect(billingpreflib.billingpref_resource.info, "billingpref.info")
cowspa.connect(billingpreflib.billingpref_resource.update, "billingpref.update")
cowspa.connect(billingpreflib.billingpref_resource.get_details, "billingpref.details")
cowspa.connect(billingpreflib.billingpref_resource.set_tax_exemption, "billingpref.set_tax_exemption")
cowspa.connect(usagelib.usage_collection.new, "usage.new")
cowspa.connect(usagelib.usage_collection.m_new, "usage.m_new")
cowspa.connect(usagelib.usage_collection.find, "usages.find")
cowspa.connect(usagelib.usage_collection.find_by_date, "usages.find_by_date")
cowspa.connect(usagelib.usage_collection.uninvoiced, "usages.uninvoiced")
cowspa.connect(usagelib.usage_collection.uninvoiced_members, "usages.uninvoiced_members")
cowspa.connect(usagelib.usage_resource.update, "usage.update")
cowspa.connect(usagelib.usage_resource.info, "usage.info")
cowspa.connect(usagelib.usage_resource.details, "usage.details")
cowspa.connect(usagelib.usage_collection.delete, "usages.delete")
cowspa.startup()
