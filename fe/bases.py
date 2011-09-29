import sphc
import sphc.more

tf = sphc.TagFactory()

webshims_base = '/js/webshims-1.8.1/'
webshims = [webshims_base + "extras/mousepress.js", webshims_base + "/extras/modernizr-custom.js", webshims_base + "/extras/loaders/sssl.js", webshims_base + "/polyfiller.js"]
ctxpath = '/%(lang)s/%(theme)s'

class CSPage(sphc.more.HTML5Page):
    jslibs = ['/js/json2.js', '/js/jquery.min.js', '/js/jquery-ui.min.js', '/js/jQuery-Timepicker-Addon/jquery-ui-timepicker-addon.js', '/js/jquery.jsonrpc.js', '/js/jquery.cookie.js', '/js/jquery.autoSuggest.js', '/js/jquery.tmpl.js', '/js/jquery.dataTables.min.js'] + webshims + ['/js/common.js']
    # loading jq locally may be we should consider do that only when remote fails
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
    def style(self):
        # .polyfill-import hack below lets password field with a placeholder to have same width as other input fields
        # which otherwise is smaller with webshims style.
        return """
        .container {
            width: 90%;
            text-align: left;
        }
        div[role="main"] { float: none;}
        .polyfill-important .placeholder-box {width: 100% !important; }
        """

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

invoicing_opt = [
    tf.A("New", href=ctxpath+'/invoicing/new', Class='navlink-opt-item'),
    tf.A("History", href=ctxpath+'/invoicing/history', Class='navlink-opt-item'),
    tf.A("Add usages", href=ctxpath+'/invoicing/addusages', Class='navlink-opt-item'),
    tf.A("Uninvoiced usages", href=ctxpath+'/invoicing/uninvoiced', Class='navlink-opt-item'),
    tf.A("Preferences", href=ctxpath+'/invoicing/preferences', Class='navlink-opt-item'),
    tf.A("Auto-Generate", hre=ctxpath+'/invoicing/auto', Class='navlink-opt-item'),
    tf.A("Export", hre=ctxpath+'/invoicing/export', Class='navlink-opt-item')
]

profile_opt = [
    tf.A("About Me", href=ctxpath + '/profile#about', Class='navlink-opt-item', id='navlink-aboutme'),
    tf.A("Memberships", href=ctxpath + '/profile#memberships', Class='navlink-opt-item', id='navlink-memberships'),
    tf.A("Contact", href=ctxpath + '/profile#contact', Class='navlink-opt-item', id='navlink-contact'),
    tf.A("Social Me", href=ctxpath + '/profile#social', Class='navlink-opt-item', id='navlink-social'),
    tf.A("Account", href=ctxpath + '/profile#account', Class='navlink-opt-item', id='navlink-account'),
    tf.A("Preferences", href=ctxpath + '/profile#preferences', Class='navlink-opt-item', id='navlink-preferences'),
    tf.A("Billing Preferences", href=ctxpath + '/profile#billingpreferences', Class='navlink-opt-item', id='navlink-billingpreferences')
    ]

resources_opt = [
    tf.A("New", href=ctxpath + '/resource/new', Class='navlink-opt-item')]

places_opt = [
    tf.A("New", href=ctxpath + '/bizplace/new', Class='navlink-opt-item'),
    tf.A("Tariffs", href=ctxpath + '/bizplace/tariffs', Class='navlink-opt-item')
    ]

new_nav = [ ('Dashboard', ctxpath + '/dashboard', None) ]
member_nav = new_nav + [
    ('Profile', '#profile', profile_opt),
    ('Members', '#', members_opt),
    ('Bookings', '#', booking_opt),
    ('Invoicing', '#', invoicing_opt), ]
host_nav = member_nav + [
    ('Places', '#', places_opt),
    ('Resources', '#', resources_opt),
    ('Reports', '#', None), ]


class CSAuthedPage(CSPage):
    top_links = [('Account', ctxpath + '/profile#account'), ('Theme', ctxpath + '/profile#preferences'), ('Logout', '/logout')]
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
    content_title = ''
    content_subtitle = ''

    def topbar(self):
        topbar = tf.DIV(Class='topbar')
        product_name = tf.DIV('c o w s p a', Class='logo')
        links = []
        for label, link in self.top_links[:-1]:
            links.append(tf.A(label, href=link, id=label.lower()))
            links.append(' | ')
        last_link = self.top_links[-1]
        links.append(tf.A(last_link[0], href=last_link[1]))

        topbar.logo = product_name
        topbar.bizplaces = tf.SELECT(id="bizplaces", name="bizplaces", style="display:none")
        topbar.links = links
        return topbar

    def main(self):
        main = tf.DIV()
        main.searchbox = tf.DIV(Class="searchbox")
        main.searchbox.content = self.search()
        main.contentbox = tf.DIV(Class="content")
        main.contentbox.title = tf.H1(self.content_title or self.title, Class="content-title")
        main.contentbox.content = self.content()
        return main

    def search(self):
        row = tf.DIV(Class="searchbox")
        cell = tf.DIV()
        cell.data = tf.SPAN("Member Search", Class="search-label", For="search")
        row.cell = cell
        cell = tf.DIV()
        cell.data = tf.INPUT(id="search", Class="search-input", type="text")
        row.cell = cell
        return row
