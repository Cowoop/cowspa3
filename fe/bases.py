import sphc
import sphc.more

tf = sphc.TagFactory()

class CSPage(sphc.more.HTML5Page):
    current_tab = 'Home'
    css_links = ['css/gridless.css', 'css/common.css']
    jslibs = sphc.more.HTML5Page.jslibs + ['js/h5f.min.js', 'js/json2.js', 'js/jquery.jsonrpc.js', 'js/common.js', 'js/knockout-1.2.1.js']

    def toplinks_bar(self):
        toplinks_container = sphc.DIV(Class='toplinks')
        toplinks_container.links = self.top_links
        return toplinks_container

class CSAnonPage(CSPage):
    top_links = [('login', '/login')]

home_opts = [(tf.A('Dashboard', '/dashboard'))]

class CSAuthedPage(CSPage):
    top_links = [('account', '/account'), ('logout', '/logout')]
    nav_links = [('Home', '/', home_opts)]


