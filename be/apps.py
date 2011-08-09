import bases.app as applib
import be.apis
import be.apis.user as userlib
import be.repository.pgdb as pgdb
import jsonrpc2

pg_provider = pgdb.PGProvider()

class CSAPIExecutor(applib.APIExecutor):
    wrappers = []

class CowspaApp(applib.Application):
    mapper = jsonrpc2.JsonRpc()
    APIExecutor = CSAPIExecutor

cowspa = CowspaApp()
cowspa.connect(userlib.login)

cowspa.startup()
