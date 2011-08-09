import bases.app as applib
import be.apis
import be.apis.user as userlib
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

cowspa.startup()
