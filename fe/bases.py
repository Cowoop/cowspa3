import sphc
import sphc.more

tf = sphc.TagFactory()

html5widget_libs = ['/js/modernizr-1.5.min.js', '/js/html5.js', '/js/EventHelpers.js', '/js/html5Widgets.js']
ctxpath = '/%(lang)s/%(theme)s'

class CSPage(sphc.more.HTML5Page):
    jslibs = html5widget_libs + sphc.more.HTML5Page.jslibs + ['/js/json2.js', '/js/jquery.jsonrpc.js', '/js/knockout-1.2.1.js', '/js/jquery.cookie.js', '/js/jquery.tokeninput.js', '/js/common.js']
    bottom_links = [('Twitter', 'http://twitter.com/cowspa'), ('API', '#API')]
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

class CSAnonPage(CSPage):
    top_links = [('login', '/login')]
    css_links = ['/themes/default/css/main.css']

members_opt = [
    #tf.INPUT(type="search", id= 'search', Class='navlink-opt-item', placeholder='Search..'),
    tf.A("New", href=ctxpath + '/member/new', Class='navlink-opt-item'),
    tf.A("Export", href=ctxpath + "/member/export", Class='navlink-opt-item')]

booking_opt = [
    #tf.INPUT(type="search", Class='navlink-opt-item', placeholder='Search..'),
    tf.A("New", href=ctxpath + '/bookings/new', Class='navlink-opt-item'),
    tf.A("My Bookings", href=ctxpath + '/bookings/mine', Class='navlink-opt-item'),
    tf.A("Calendar", href=ctxpath + '/bookings/calendar', Class='navlink-opt-item'),
    tf.A("Agenda", href=ctxpath + "/bookings/agenda", Class='navlink-opt-item'),
    tf.A("Events", href=ctxpath + "/bookings/events", Class='navlink-opt-item'),
    tf.A("Export", href=ctxpath + "/bookings/export", Class='navlink-opt-item'),
    ]

invoicing_opt = None

profile_opt = [
    tf.A("About Me", href=ctxpath + '/profile#about', Class='navlink-opt-item', id='navlink-aboutme'),
    tf.A("Account", href=ctxpath + '/profile#account', Class='navlink-opt-item', id='navlink-account'),
    tf.A("Social Me", href=ctxpath + '/profile#social', Class='navlink-opt-item', id='navlink-social'),
    tf.A("Contact", href=ctxpath + '/profile#contact', Class='navlink-opt-item', id='navlink-contact')
    ]
    
resources_opt = [
    tf.A("New", href=ctxpath + '/resource/create', Class='navlink-opt-item')]

places_opt = [
    tf.A("New", href=ctxpath + '/bizplace/create', Class='navlink-opt-item')]
        
class CSAuthedPage(CSPage):
    top_links = [('Account', ctxpath + '/profile#account'), ('Theme', '#themes'), ('Logout', '/logout')]
    css_links = [ '/themes/%(theme)s/css/main.css' ]
    nav_menu = [
        ('Dashboard', ctxpath + '/dashboard', None),
        ('Profile', '#profile', profile_opt),
        ('Members', '#', members_opt),
        ('Bookings', '#', booking_opt),
        ('Invoicing', '#', invoicing_opt),
        ('Places', '#', places_opt),
        ('Resources', '#', resources_opt),
        ('Reports', '#', None),
        ]
    current_nav = '/Dashboard'

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
        
    def searchbox(self):
        searchbox = tf.DIV(Class='searchbox')
        searchbox.div = tf.DIV(Class='search')
        searchbox.div.input = tf.INPUT(id="search", type="text")
        return searchbox
