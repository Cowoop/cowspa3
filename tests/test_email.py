def test():
    config = {
        'mail.on': True,
        'mail.transport': 'smtp',
        'mail.smtp.server': 'smtp.gmail.com',
        'mail.smtp.port': 587,
        'mail.smtp.tls': True,
        'mail.smtp.username': 'me@gmail.com',
        'mail.smtp.password': 'secret',
        'mail.smtp.debug': True,
        'mail.utf8qp.on': True
    }
    mailer = Mailer(config)
    to = "to.me@gmail.com"
    subject = "TurboMail test"
    rich = """
    <html>
        <body>
            <strong>Hi There</strong>
        </body>
    </html>"""
    mailer.start()
    mailer.send("to.me@gmail.com", to, subject, rich=rich)
