import be.bootstrap
be.bootstrap.start('conf_test')
import be.apps
app = be.apps.cowspa
app.tr_start()
app.mapper['setup']('shon', 'x', 'test@example.com', 'Shekhar')
app.tr_complete()
