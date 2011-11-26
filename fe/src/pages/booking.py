import sphc
import fe.bases

tf = sphc.TagFactory()
BasePage = fe.bases.CSAuthedPage

min15 = lambda: tf.DIV(Class='cal-min15')

def hourrange(start, end):
    return ((((hr or 12) if hr < 12 else ((hr - 12) or hr)), ('AM' if hr < 12 else 'PM')) for hr in range(start, end))

def timecolumn(start, end):
    return tf.DIV([tf.DIV('%d %s' % hr, Class='cal-hour') for hr in hourrange(start, end)], Class='cal-day')

def day():
    slots = [min15() for i in range(24*4)] # 4 15mins * 24 hours
    for i, slot in enumerate(slots):
        remainder = (i%4)
        if not remainder:
            slot.add_classes(['hour-start'])
        elif remainder == 3:
            slot.add_classes(['hour-end'])
    cells = [tf.DIV("title", Class='day-title', id="day-${day_id}")] + slots
    return tf.DIV(cells, Class='cal-day')

def week():
    return [tf.DIV([timecolumn(0, 24)] + [day() for x in range(7)], Class='cal-week')]

class Booking(BasePage):
    current_nav = 'Bookings'
    title = 'Booking'

    def content(self):
        container = tf.DIV()

        resource_pane = tf.DIV(id="pane-resource")
        resource_pane.resource_opt = sphc.more.jq_tmpl('resource-opt')
        resource_pane.resource_opt.opt = tf.OPTION()
        resource_pane.select = tf.SELECT(id='resource-select')
        resource_pane.select.option = tf.OPTION("Select a resource", disabled="true", selected="selected")
        resource_pane.date_vis = tf.SPAN(type="text", id="booking-date-inp-vis", placeholder="Select booking date")
        resource_pane.date = tf.INPUT(type="hidden", id="booking-date-inp")

        booking_pane = tf.DIV(id="pane-booking")
        booking_pane.topbar = tf.DIV(id="booking-menu")
        booking_pane.calendar = tf.DIV(id="booking-cal")

        calendar = booking_pane.calendar
        calendar.week = week()

        container.resource_pane = resource_pane
        container.booking_pane = booking_pane

        container.script = sphc.more.script_fromfile("fe/src/js/booking.js")

        return container
