import sphc
import fe.bases

tf = sphc.TagFactory()
BasePage = fe.bases.CSAuthedPage

min15 = lambda x, y: tf.DIV(Class='cal-min15', id="slot_%s-%s" % (x,y))

def hourrange(start, end):
    return ((((hr or 12) if hr < 12 else ((hr - 12) or hr)), ('AM' if hr < 12 else 'PM')) for hr in range(start, end))

def timecolumn(start, end):
    return tf.DIV([tf.DIV('%d %s' % hr, Class='cal-hour') for hr in hourrange(start, end)], Class='cal-day')

def day(day_no):
    slots = [min15(day_no, i) for i in range(24*4)] # 4 15mins * 24 hours
    for i, slot in enumerate(slots):
        remainder = (i%4)
        if not remainder:
            slot.add_classes(['hour-start'])
        elif remainder == 3:
            slot.add_classes(['hour-end'])
    cells = [tf.DIV("title", Class='day-title', id="day-title_%s" % day_no)] + slots
    return tf.DIV(cells, Class='cal-day', id="day_%s" % day_no)

def week():
    return [tf.DIV([timecolumn(0, 24)] + [day(i) for i in range(7)], Class='cal-week')]

class Booking(BasePage):
    current_nav = 'Bookings'
    title = 'Booking'

    def content(self):
        container = tf.DIV()

        resource_pane = tf.DIV(id="pane-resource")
        resource_pane.resource_opt = sphc.more.jq_tmpl('resource-opt')
        resource_pane.resource_opt.opt = tf.OPTION("${name}", value="${id}")
        resource_pane.date = tf.SPAN(type="text", id="booking-date-inp")
        resource_pane.select = tf.SELECT(id='resource-select')
        resource_pane.select.option = tf.OPTION("Select a resource", disabled="true", selected="selected")

        booking_pane = tf.DIV(id="pane-booking")
        booking_pane.topbar = tf.DIV(id="booking-menu")
        booking_pane.calendar = tf.DIV(id="booking-cal")

        calendar = booking_pane.calendar
        calendar.week = week()

        container.resource_pane = resource_pane
        container.booking_pane = booking_pane

        container.script = sphc.more.script_fromfile("fe/src/js/booking.js")

        return container
