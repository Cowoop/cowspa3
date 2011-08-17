import sphc
import sphc.more

tf = sphc.TagFactory()

html5widget_libs = ['/js/modernizr-1.5.min.js', '/js/html5.js', '/js/EventHelpers.js', '/js/html5Widgets.js']

class CSPage(sphc.more.HTML5Page):
    current_tab = 'Home'
    css_links = ['/css/emastic-type.css', '/css/common.css', '/css/grid.css']
    jslibs = html5widget_libs + sphc.more.HTML5Page.jslibs + ['/js/json2.js', '/js/jquery.jsonrpc.js', '/js/common.js', '/js/knockout-1.2.1.js', '/js/jquery.cookie.js']

class CSAnonPage(CSPage):
    top_links = [('login', '/login')]

members_opt = [
    tf.INPUT(type="search", Class='navlink-opt-item', placeholder='Search..'),
    tf.A("New", href='/member/new', Class='navlink-opt-item'),
    tf.A("Export", href="/member/export", Class='navlink-opt-item')]

booking_opt = [
    tf.INPUT(type="search", Class='navlink-opt-item', placeholder='Search..'),
    tf.A("New", href='/bookings/new', Class='navlink-opt-item'),
    tf.A("My Bookings", href='/bookings/mine', Class='navlink-opt-item'),
    tf.A("Calendar", href='/bookings/calendar', Class='navlink-opt-item'),
    tf.A("Agenda", href="/bookings/agenda", Class='navlink-opt-item'),
    tf.A("Events", href="/bookings/events", Class='navlink-opt-item'),
    tf.A("Export", href="/bookings/export", Class='navlink-opt-item'),
    ]

invoicing_opt = None

class CSAuthedPage(CSPage):
    top_links = [('account', '/account'), ('logout', '/logout')]
    nav_links = [
        ('Dashboard', '#/dashboard', None),
        ('Profile', '#/profile', None),
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
