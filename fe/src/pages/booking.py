import sphc
import sphc.more
import fe.bases

tf = sphc.TagFactory()
BasePage = fe.bases.CSAuthedPage

min2str = lambda m: "%02d:%02d" % ((m / 60), (m % 60))
min15 = lambda day, minute: tf.DIV(Class='cal-min15 slot-available', id="slot_%s-%s.%s" % (day, min2str(minute), min2str(minute+15)))

def hourrange(start, end):
    return ((((hr or 12) if hr < 12 else ((hr - 12) or hr)), ('AM' if hr < 12 else 'PM')) for hr in range(start, end))

def timecolumn(start, end):
    return tf.DIV([tf.DIV(Class="time-title")]+[tf.DIV('%d %s' % hr, Class='cal-hour') for hr in hourrange(start, end)], Class='time-column')

def day(day_no):
    slots = [min15(day_no, (i*15)) for i in range(24*4)] # 4 15mins * 24 hours
    for i, slot in enumerate(slots):
        remainder = (i%4)
        if not remainder:
            slot.add_classes(['hour-start'])
        elif remainder == 3:
            slot.add_classes(['hour-end'])
    cells = [tf.DIV("title", Class='day-title slot-unavailable', id="day-title_%s" % day_no)] + slots
    return tf.DIV(cells, Class='cal-day', id="day_%s" % day_no)

def week():
    return [tf.DIV([timecolumn(0, 24)] + [day(i) for i in range(7)], Class='cal-week')]

def booking_form():
    form = sphc.more.Form(id='new-booking-form', Class='vform')
    #form.add(tf.DIV(Class='heading3 data-resource-name'))
    #form.add(tf.HR())
    form.add(tf.DIV(id="new-booking-date"))
    form.add(tf.INPUT(id="booking-id", type="hidden"))
    form.add(tf.INPUT(id="for-member", type="hidden"))
    form.add_field("Member name", tf.INPUT(id="for-member-search").set_required(), "Type to autocomplete member name")
    form.add_field("Starts", tf.INPUT(id="new-starts", type="time", step="900").set_required(), "Use arrow keys to change values")
    form.add_field("Ends", tf.INPUT(id="new-ends", type="time", step="900"))
    #form.add_field("Quantity", tf.INPUT(id="new-quantity", type="text"), "Not applicable for time based resources")
    form.add_buttons(tf.INPUT(type="submit", value="Save"))
    return form.build()

class BookingPage(BasePage):
    current_nav = 'Bookings'
    title = 'Bookings'
    content_menu = [tf.A('+ New', href="/${lang}/${theme}/booking/new", Class="item"),
        tf.C('|', Class="item-w"),
        tf.C('Agenda', Class="item"),
        tf.A("Week", href="/${lang}/${theme}/booking/week", Class="item"),
        #tf.A("Month", href="/${lang}/${theme}/booking/month", Class="item")
        ]

class Booking(BookingPage):
    def content(self):
        container = tf.DIV()

        resource_pane = tf.DIV(id="pane-resource")
        resource_pane.resource_opt = sphc.more.jq_tmpl('resource-opt')
        resource_pane.resource_opt.opt = tf.OPTION("${name}", value="${id}")
        resource_pane.select = tf.SELECT(id='resource-select')
        resource_pane.select.option = tf.OPTION("Select a resource", disabled="true", selected="selected")
        resource_pane.date = tf.SPAN(id="booking-date-inp")

        booking_pane = tf.DIV(id="pane-booking")
        booking_pane.topbar = tf.DIV(id="booking-menu")
        booking_pane.new_booking = tf.DIV(id="new-booking", Class="hidden")
        booking_pane.new_booking.form = booking_form()
        booking_pane.calendar = tf.DIV(id="booking-cal", Class="opaq")

        calendar = booking_pane.calendar
        calendar.week = week()

        container.resource_pane = resource_pane
        container.booking_pane = booking_pane

        container.script = sphc.more.script_fromfile("fe/src/js/booking.js")

        return container

class WeekAgenda(BookingPage):
    def content(self):
        container = tf.DIV(id="agenda")

        resource_pane = tf.DIV(id="pane-resource")
        #resource_pane.monthselector = tf.INPUT(id="month-picker", type="text", placeholder="Select Month")
        resource_pane.date = tf.SPAN(type="text", id="booking-date-inp")
        #resource_pane.monthselector = tf.DIV(id="month-picker")
        #resource_pane.monthselector = tf.INPUT(id="month-selected", type="hidden")

        booking_pane = tf.DIV(id="pane-booking")
        bookings_tmpl = sphc.more.jq_tmpl('bookings-tmpl')
        bookings_tmpl.aday = tf.DIV(Class="aday")
        bookings_tmpl.aday.date = tf.DIV(Class="date")
        bookings_tmpl.aday.date.year = tf.SPAN("${format_date(iso2date(date), 'DD')}", Class="year")
        bookings_tmpl.aday.date.day = tf.SPAN("${iso2date(date).getDate()}", Class="day")
        bookings_tmpl.aday.date.month = tf.SPAN("${format_date(iso2date(date), 'MM')}", Class="month")
        bookings_tmpl.aday.bookings = tf.DIV(Class="data")
        bookings_tmpl.aday.bookings.loop_start = "{{each bookings}}"
        bookings_tmpl.aday.bookings.booking = tf.DIV(Class="booking")
        bookings_tmpl.aday.bookings.booking.timw = tf.DIV("${iso2ftime(start_time)} - ${iso2ftime(end_time)}")
        bookings_tmpl.aday.bookings.booking.name = tf.DIV("${resource_name}", Class="name")
        bookings_tmpl.aday.bookings.booking.member = tf.DIV("Booked for: ${member_name}", Class="member-name")
        bookings_tmpl.aday.bookings.booking.member = tf.DIV("Booked by: ${created_by_name}", Class="member-name")
        bookings_tmpl.aday.bookings.loop_end = "{{/each}}"

        container.resource_pane = resource_pane
        container.booking_pane = booking_pane
        container.bookings_tmpl = bookings_tmpl
        #container.mp_script = tf.SCRIPT(src='https://raw.github.com/lucianocosta/jquery.mtz.monthpicker/master/jquery.mtz.monthpicker.js')
        #container.mp_script = tf.SCRIPT(src='http://ec2-46-137-53-243.eu-west-1.compute.amazonaws.com/jquery-ui-monthpicker/jquery.ui.monthpicker.js')
        container.script = sphc.more.script_fromfile("fe/src/js/booking_agenda.js")

        return container
