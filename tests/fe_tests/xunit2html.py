from xml.etree.ElementTree import ElementTree as ET
import sphc 

tf = sphc.TagFactory()
html = tf.HTML()
html.head = tf.HEAD()
html.body = tf.BODY()

html.body.content = tf.H2("Summary")

html.body.content.br = tf.BR()

summary_tab = tf.TABLE(BORDER="2",BORDERCOLOR="#336699",CELLPADDING="2", CELLSPACING="2")
tree=ET()
ts = tree.parse('nosetests.xml')
for at in ts.keys():
    row = tf.TR()
    row.cells = [tf.TD(at), tf.TD(ts.get(at))]
    summary_tab.row = row

html.body.content.atable = summary_tab

html.body.content.h2 = tf.H2("Details")

details_tab = tf.TABLE(BORDER="2",BORDERCOLOR="#336699",CELLPADDING="2", CELLSPACING="2")
row = tf.TR()
row.cells = [tf.TD('name'), tf.TD('Result'),tf.TD('Error Message'),tf.TD('time')]
details_tab.row = row

for tc in ts.findall('testcase'):
    result = 'Passed'
    err_msg = ' '
    fl = tc.find('failure')
    if fl is not None:
        result = 'Failed'
        err_msg = eval(fl.get('message').split('\n')[0]).get(u'debug')

    row = tf.TR()
    row.cells = [tf.TD(tc.get('name')), 
                 tf.TD(result),
                 tf.TD(err_msg),
                 tf.TD(tc.get('time'))]
    details_tab.row = row

html.body.content.atable = details_tab

print html

