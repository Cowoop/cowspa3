# -*- coding: UTF-8 -*-
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
    tf.A("Memberships", href=ctxpath + '/member/memberships', Class='navlink-opt-item'),
    tf.A("Manage Profile", href=ctxpath + '/member/edit', Class='navlink-opt-item'),
    tf.A("Announce", href=ctxpath + '/member/edit', Class='navlink-opt-item'),
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
    tf.A("Received", href=ctxpath+'/invoicing/sent', Class='navlink-opt-item'),
    tf.A("Sent", href=ctxpath+'/invoicing/history', Class='navlink-opt-item'),
    tf.A("Settings", href=ctxpath+'/invoicing/preferences', Class='navlink-opt-item'),
    tf.A("Auto-Generate", hre=ctxpath+'/invoicing/auto', Class='navlink-opt-item'),
    tf.A("Export", hre=ctxpath+'/invoicing/export', Class='navlink-opt-item')
]

profile_opt = [
    tf.A("About Me", href=ctxpath + '/profile#about', Class='navlink-opt-item', id='navlink-aboutme'),
    tf.A("Contact", href=ctxpath + '/profile#contact', Class='navlink-opt-item', id='navlink-contact'),
    tf.A("Billing Preferences", href=ctxpath + '/profile#billingpreferences', Class='navlink-opt-item', id='navlink-billingpreferences'),
    tf.A("Social Me", href=ctxpath + '/profile#social', Class='navlink-opt-item', id='navlink-social'),
    tf.A("Memberships", href=ctxpath + '/profile#memberships', Class='navlink-opt-item', id='navlink-memberships'),
    tf.A("Account", href=ctxpath + '/profile#account', Class='navlink-opt-item', id='navlink-account'),
    tf.A("Preferences", href=ctxpath + '/profile#preferences', Class='navlink-opt-item', id='navlink-preferences'),
    ]

resources_opt = [
    tf.A("New", href=ctxpath + '/resource/new', Class='navlink-opt-item'),
    tf.A("Manage", href=ctxpath + '/resource/list', Class='navlink-opt-item')
    ]

locations_opt = [
    tf.A("New", href=ctxpath + '/bizplace/new', Class='navlink-opt-item'),
    tf.A("Tariffs", href=ctxpath + '/bizplace/tariffs', Class='navlink-opt-item')
    ]

new_nav = [ ('Dashboard', ctxpath + '/dashboard', []) ]
member_nav = new_nav + [
    ('Profile', '#profile', profile_opt),
    ('Members', '#', members_opt),
    ('Bookings', '#', booking_opt),
    ('Invoicing', '#', invoicing_opt), ]
host_nav = member_nav + [
    ('Locations', '#', locations_opt),
    ('Resources', '#', resources_opt),
    ('Reports', '#', []), ]


class CSAuthedPage(CSPage):
    top_links = [('Account', ctxpath + '/profile#account'), ('Theme', ctxpath + '/profile#preferences'), ('Logout', '/logout')]
    css_links = [ 'http://fonts.googleapis.com/css?family=Ubuntu:300,300italic,400,400italic,500,500italic,700,700italic&amp;subset=latin,greek,cyrillic', '/themes/%(theme)s/css/main.css' ]
    nav_menu = [
        ('Dashboard', ctxpath + '/dashboard', []),
        ('My Profile', '#profile', profile_opt),
        ('Members', '#', members_opt),
        ('Bookings', '#', booking_opt),
        ('Invoicing', '#', invoicing_opt),
        ('Resources', '#', resources_opt),
        ('Locations', '#', locations_opt),
        ('Reports', '#', []),
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

    def nav(self):
        if not self.nav_menu: return ''
        nav = tf.NAV()
        nav.context_opt = sphc.more.jq_tmpl("context-opt-tmpl")
        nav.context_opt.opt = tf.OPTION("${label}", value="${id}")
        nav.context_box = tf.SPAN()
        nav.context_box.selector = tf.SELECT(id="context-select")
        menu = tf.DIV(Class="menu")
        submenu_container = tf.DIV(Class="submenu-container")
        for m_id, (label, url, submenu) in enumerate(self.nav_menu):
            menu_item = tf.DIV(Class="menu-item", id="menu-item_%s" % m_id) # nav
            menu_item.link = tf.A(label, href=url)
            if label == self.current_nav:
                menu_item.add_classes(["current"])
            if submenu:
                submenu_box = tf.DIV(Class="submenu-box", id="submenu_%s" % m_id)
                for item in submenu:
                    smi_box = tf.DIV(item, Class="submenu-item")
                    if label == self.current_nav:
                        smi_box.add_classes(["current"])
                    submenu_box.smi_box = smi_box
                submenu_container.submenu_box = submenu_box
            menu.item = menu_item
        nav.menu = menu
        nav.submenu = submenu_container
        return nav

    def main(self):
        main = tf.DIV()
        main.clear = sphc.more.clear()
        main.clear = tf.C('.', style="opacity:0;")
        main.searchbox = tf.DIV(Class="searchbox")
        main.searchbox.content = self.search()
        main.contentbox = tf.DIV(Class="content")
        main.contentbox.title = tf.H1(self.content_title or self.title, Class="content-title")
        main.contentbox.content = self.content()
        return main

    def search(self):
        row = tf.DIV()
        cell = tf.DIV()
        cell.data = tf.SPAN("Member Search..", Class="search-label", For="search")
        row.cell = cell
        cell = tf.DIV()
        cell.data = tf.INPUT(id="search", Class="search-input", type="text")
        row.cell = cell
        return row
