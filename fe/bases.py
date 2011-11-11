# -*- coding: UTF-8 -*-
import sphc
import sphc.more

tf = sphc.TagFactory()

webshims_base = '/js/webshims-1.8.2'
webshims = [webshims_base + "/extras/modernizr-custom.js", webshims_base + "/polyfiller.js"]
ctxpath = '/%(lang)s/%(theme)s'

class CSPage(sphc.more.HTML5Page):
    jslibs = ['/js/json2.js', '/js/jquery.min.js', '/js/jquery-ui.min.js', '/js/jQuery-Timepicker-Addon/jquery-ui-timepicker-addon.js', '/js/jquery.jsonrpc.js', '/js/jquery.cookie.js', '/js/jquery.autoSuggest.js', '/js/jquery.tmpl.js', '/js/jquery.dataTables.min.js'] + webshims + ['/js/SS.min.js', '/js/common.js']
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
    #tf.INPUT(type="search", id= 'search', placeholder='Search..'),
    tf.A("New", href=ctxpath + '/member/new'),
    tf.A("Manage Profile", href=ctxpath + '/member/edit'),
    tf.A("Memberships", href=ctxpath + '/member/memberships'),
    tf.A("Announce", href='#' + ctxpath + '/member/announce'),
    tf.A("Export", href='#' + ctxpath + "/member/export")]

booking_opt = [
    #tf.INPUT(type="search", placeholder='Search..'),
    tf.A("New", href='#/' + ctxpath + '/bookings/new'),
    tf.A("My Bookings", href='#/' + ctxpath + '/bookings/mine'),
    tf.A("Calendar", href='#/' + ctxpath + '/bookings/calendar'),
    tf.A("Agenda", href='#/' + ctxpath + "/bookings/agenda"),
    tf.A("Events", href='#/' + ctxpath + "/bookings/events"),
    tf.A("Export", href='#/' + ctxpath + "/bookings/export"),
    ]

invoicing_opt = [
    tf.A("New", href=ctxpath+'/invoicing/new'),
    tf.A("Sent", href=ctxpath+'/invoicing/history'),
    tf.A("Received", href='#'),
    tf.A("Settings", href=ctxpath+'/invoicing/preferences'),
    tf.A("Auto-Generate", href='#'),
    tf.A("Export", href='#')
]

resources_opt = [
    tf.A("New", href=ctxpath + '/resource/new'),
    tf.A("Manage", href=ctxpath + '/resource/list')
    ]

locations_opt = [
    tf.A("New", href=ctxpath + '/bizplace/new'),
    tf.A("Tariffs", href=ctxpath + '/bizplace/tariffs'),
    tf.A("List", href=ctxpath + '/bizplaces')
    ]

new_nav = [ ('Dashboard', ctxpath + '/dashboard', []) ]
member_nav = new_nav + [
    ('Members', '#', members_opt),
    ('Bookings', '#', booking_opt),
    ('Invoicing', '#', invoicing_opt), ]
host_nav = member_nav + [
    ('Locations', '#', locations_opt),
    ('Resources', '#', resources_opt),
    ('Reports', '#', []), ]


class CSAuthedPage(CSPage):
    top_links = [('Profile_Link', ctxpath + ''), ('Logout', '/logout')]
    css_links = [ 'http://fonts.googleapis.com/css?family=Ubuntu:300,300italic,400,400italic,500,500italic,700,700italic&amp;subset=latin,greek,cyrillic', '/themes/%(theme)s/css/main.css' ]
    nav_menu = [
        ('Dashboard', ctxpath + '/dashboard', []),
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
        nav.context_box.single_context = tf.SPAN(id="context-single")
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
        #main.clear = tf.C('.', style="opacity:0;")
        main.searchbox = tf.DIV(Class="searchbox")
        main.searchbox.content = self.search()
        main.contentbox = tf.DIV(Class="content")
        title = self.content_title or self.title or ''
        if title:
            title += ' '
            title_classes = "content-title"
        else:
            title_classes = "content-title hidden"
        main.contentbox.title = tf.DIV([tf.c(title, id="content-title"), tf.SPAN(Class="content-subtitle")], Class=title_classes)
        main.contentbox.content = self.content()
        return main

    def search(self):
        container = tf.DIV()
        container.search_box = tf.DIV(Class="search-box")
        container.search_box.label = tf.SPAN(tf.LABEL("Member Search ", For="search"))
        container.search_box.cell = tf.SPAN(tf.INPUT(id="search", type="text"), Class="search-input")
        return container

