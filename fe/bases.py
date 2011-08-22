import sphc
import sphc.more

tf = sphc.TagFactory()

html5widget_libs = ['/js/modernizr-1.5.min.js', '/js/html5.js', '/js/EventHelpers.js', '/js/html5Widgets.js']
ctxpath = '/%(lang)s/%(theme)s'

class CSPage(sphc.more.HTML5Page):
    current_tab = 'Home'
    jslibs = html5widget_libs + sphc.more.HTML5Page.jslibs + ['/js/json2.js', '/js/jquery.jsonrpc.js', '/js/knockout-1.2.1.js', '/js/jquery.cookie.js', '/js/jquery.tokeninput.js', '/js/common.js']
    bottom_links = [('Twitter', 'http://twitter.com/cowspa'), ('API', '#API')]

class CSAnonPage(CSPage):
    top_links = [('login', '/login')]
    css_links = ['/themes/default/css/main.css']

members_opt = [
    tf.INPUT(type="search", id= 'search', Class='navlink-opt-item', placeholder='Search..'),
    tf.A("New", href=ctxpath + '/member/new', Class='navlink-opt-item'),
    tf.A("Export", href=ctxpath + "/member/export", Class='navlink-opt-item')]

booking_opt = [
    tf.INPUT(type="search", Class='navlink-opt-item', placeholder='Search..'),
    tf.A("New", href=ctxpath + '/bookings/new', Class='navlink-opt-item'),
    tf.A("My Bookings", href=ctxpath + '/bookings/mine', Class='navlink-opt-item'),
    tf.A("Calendar", href=ctxpath + '/bookings/calendar', Class='navlink-opt-item'),
    tf.A("Agenda", href=ctxpath + "/bookings/agenda", Class='navlink-opt-item'),
    tf.A("Events", href=ctxpath + "/bookings/events", Class='navlink-opt-item'),
    tf.A("Export", href=ctxpath + "/bookings/export", Class='navlink-opt-item'),
    ]

invoicing_opt = None

class CSAuthedPage(CSPage):
    top_links = [('Account', ctxpath + '/account'), ('Theme', '#themes'), ('Logout', '/logout')]
    css_links = [ '/themes/%(theme)s/css/main.css']
    nav_links = [
        ('Dashboard', '#dashboard', None),
        ('Profile', '#profile', None),
        ('Members', '#', members_opt),
        ('Bookings', '#', booking_opt),
        ('Invoicing', '#', invoicing_opt),
        ('Places', '#', None),
        ('Resources', '#', None),
        ('Reports', '#', None),
        ]
    def topbar(self):
        topbar = tf.DIV(Class='topbar')
        product_name = tf.DIV('c o w s p a', Class='logo')
        links = []
        for label, link in self.top_links[:-1]:
            links.append(tf.A(label, href=link))
            links.append(' | ')
        last_link = self.top_links[-1]
        links.append(tf.A(last_link[0], href=last_link[1]))

        topbar.logo = product_name
        topbar.links = links
        return topbar
    def bottombar(self):
        bar = tf.DIV(Class='bottombar')
        links = []
        for label, link in self.bottom_links[:-1]:
            links.append(tf.A(label, href=link))
            links.append(' | ')
        last_link = self.bottom_links[-1]
        links.append(tf.A(last_link[0], href=last_link[1]))
        bar.links = links
        return bar
