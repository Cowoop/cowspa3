import os
import datetime
import commontest
import commonlib.helpers

def setup():
    commontest.setup_test_env()

def test_html2pdf():
    cur_datetime = datetime.datetime.now()
    html_file = "tests/%s.html" % cur_datetime
    pdf_file = "tests/%s.pdf" % cur_datetime
    open(html_file, 'w').write("<html><body>Done</body></html>")
    assert commonlib.helpers.html2pdf(html_file, pdf_file)
    assert os.path.isfile(pdf_file)
    os.remove(html_file)
    os.remove(pdf_file)
