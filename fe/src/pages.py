import fe.bases

BasePage = fe.bases.CSAuthedPage

class InvoicingPage(BasePage):
    current_tab = 'invoicing'
    title = 'Invoicing'
    def  main(self):
        return ''
