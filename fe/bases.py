import sphc
import sphc.more

class CSPage(sphc.more.HTML5Page):
    current_tab = 'Home'

    def toplinks_bar(self):
        toplinks_container = sphc.DIV(Class='toplinks')
        toplinks_container.links = self.top_links
        return toplinks_container

class CSAnonPage(CSPage):
    top_links = [('login', '/login')]

class CSAuthedPage(CSPage):
    top_links = [('account', '/account'), ('logout', '/logout')]


