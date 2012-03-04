import sphc
import sphc.more
import fe.bases

tf = sphc.TagFactory()
BasePage = fe.bases.CSAuthedPage
ctxpath = fe.bases.ctxpath

min2str = lambda m: "%02d:%02d" % ((m / 60), (m % 60))
min15 = lambda day, minute: tf.DIV(Class='cal-min15 slot-available', id="slot_%s-%s.%s" % (day, min2str(minute), min2str(minute+15)))
start_hour = 7

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
        if i < (4*start_hour):
            slot.add_classes(['hidden'])
    cells = [tf.DIV("title", Class='day-title slot-unavailable', id="day-title_%s" % day_no)] + slots
    return tf.DIV(cells, Class='cal-day', id="day_%s" % day_no)

def week():
    return [tf.DIV([timecolumn(start_hour, 24)] + [day(i) for i in range(7)], Class='cal-week')]

def member_booking_form():
    form = sphc.more.Form(id="new-booking-form", Class='hform')

    form.add(tf.DIV([tf.SPAN(id="new-booking-date"), tf.SPAN(tf.BUTTON("Cancel", id="booking-delete"), Class="booking-delete-section hidden")]))
    form.add(tf.INPUT(id="booking-id", type="hidden"))
    form.add_field("Booking name", tf.INPUT(id="booking-name", type="text"))
    form.add_field("Publicise event", tf.INPUT(id="booking-public", type="CHECKBOX"))
    form.add_field("Booking description", tf.TEXTAREA(id="booking-description"))
    form.add_field("Starts", tf.INPUT(id="new-starts", type="time", step="900").set_required(), "Use arrow keys to change values")
    form.add_field("Ends", tf.INPUT(id="new-ends", type="time", step="900"))
    form.add_field("Additional Information", tf.TEXTAREA(id="booking-notes"))
    form.add_field("Number of People", tf.INPUT(type='number', value='0', id="booking-no_of_people"))
    form.add_field("Cost", tf.C(id="booking-cost"))

    extras = sphc.more.Fieldset()
    extras.add(tf.LEGEND("Extras"))
    extras.add(tf.DIV(id='contained-usages'))
    extras.add(tf.DIV(id='suggested-usages'))

    form.add(extras)

    form.add_buttons(tf.INPUT(type="submit", value="Save"))
    return form.build()

def host_booking_form():
    form = sphc.more.Form(id="new-booking-form", Class='hform')

    booking = form.add(sphc.more.Fieldset())
    booking.add(tf.DIV([tf.SPAN(id="new-booking-date"), tf.SPAN(tf.BUTTON("Cancel", id="booking-delete"), Class="booking-delete-section hidden")]))
    booking.add(tf.LEGEND("Booking"))
    booking.add(tf.INPUT(id="booking-id", type="hidden"))
    booking.add_field("Booking name", tf.INPUT(id="booking-name", type="text"))
    booking.add_field("Publicise event", tf.INPUT(id="booking-public", type="CHECKBOX"))
    booking.add_field("Booking description", tf.TEXTAREA(id="booking-description"))
    booking.add(tf.INPUT(id="for-member", type="hidden"))
    booking.add_field("Member name", tf.INPUT(id="for-member-search").set_required(), "Type to autocomplete member name")
    booking.add_field("Starts", tf.INPUT(id="new-starts", type="time", step="900").set_required(), "Use arrow keys to change values")
    booking.add_field("Ends", tf.INPUT(id="new-ends", type="time", step="900"))
    booking.add_field("Additional Information", tf.TEXTAREA(id="booking-notes"))
    booking.add_field("Number of People", tf.INPUT(type='number', value='0', id="booking-no_of_people"))
    booking.add_field("Cost", tf.INPUT(type='text', id="booking-cost"), "Leave blank for automatic calculation")

    usages = form.add(sphc.more.Fieldset())
    usages.add(tf.LEGEND("Extras"))
    usages.add(tf.DIV(id='contained-usages'))
    usages.add(tf.DIV(id='suggested-usages'))

    form.add_buttons(tf.INPUT(type="submit", value="Save"))
    return form.build()


class BookingPage(BasePage):
    current_nav = 'Bookings'
    title = 'Bookings'
    content_menu = [tf.A('+ New', href=ctxpath + "/booking/new", Class="item"),
        tf.C('|', Class="item-w"),
        tf.C('Agenda', Class="item"),
        tf.A("Week", href=ctxpath + "/booking/week", Class="item"),
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

        contained_usages_tmpl = sphc.more.jq_tmpl('contained-usages-tmpl')
        contained_usages_tmpl.usage = tf.DIV(Class='field')
        contained_usages_tmpl.usage.label = tf.DIV('${name} (${locale_data.currency_symbol} ${price})', Class='field-label')
        contained_usages_tmpl.usage.cond = '{{if (calc_mode == 0)}}'
        contained_usages_tmpl.usage.value = tf.DIV(tf.INPUT(type='number', min='1', value='1', Class='selected-usage-resources', id='resource-${id}'), Class='field-input')
        contained_usages_tmpl.usage.cond_end = '{{/if}}'
        contained_usages_tmpl.usage.cond = '{{if (calc_mode == 1)}}'
        contained_usages_tmpl.usage.value = tf.DIV(tf.INPUT(type='CHECKBOX', checked='1', disabled='1', Class='selected-usage-resources', id='resource-${id}'), Class='field-input')
        contained_usages_tmpl.usage.cond_end = '{{/if}}'

        suggested_usages_tmpl = sphc.more.jq_tmpl('suggested-usages-tmpl')
        suggested_usages_tmpl.usage = tf.DIV(Class='field')
        suggested_usages_tmpl.usage.label = tf.DIV('${name} (${locale_data.currency_symbol} ${price})', Class='field-label')
        suggested_usages_tmpl.usage.cond = '{{if (calc_mode == 0)}}'
        suggested_usages_tmpl.usage.value = tf.DIV(tf.INPUT(type='number', value="0", Class='selected-usage-resources', id='resource-${id}'), Class='field-input')
        suggested_usages_tmpl.usage.cond_end = '{{/if}}'
        suggested_usages_tmpl.usage.cond = '{{if (calc_mode == 1)}}'
        suggested_usages_tmpl.usage.value = tf.DIV(tf.INPUT(type='CHECKBOX', Class='selected-usage-resources', id='resource-${id}'), Class='field-input')
        suggested_usages_tmpl.usage.cond_end = '{{/if}}'

        booking_pane = tf.DIV(id="pane-booking")
        booking_pane.topbar = tf.DIV(id="booking-menu")
        booking_pane.new_booking = tf.DIV(id="new-booking", Class="hidden")
        if self.data['role'] in ('host', 'director', 'admin'):
            booking_pane.new_booking.form = host_booking_form()
        else:
            booking_pane.new_booking.form = member_booking_form()
        booking_pane.calendar = tf.DIV(id="booking-cal", Class="opaq")
        booking_pane.contained_usages_tmpl = contained_usages_tmpl
        booking_pane.suggested_usages_tmpl = suggested_usages_tmpl

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
        bookings_tmpl.aday.bookings.booking.time = tf.DIV("${iso2ftime(start_time)} - ${iso2ftime(end_time)}")
        bookings_tmpl.aday.bookings.booking.name = tf.DIV("${resource_name}", Class="name")
        bookings_tmpl.aday.bookings.booking.member = tf.DIV("Booked for: ${member_name}", Class="member-name")
        bookings_tmpl.aday.bookings.booking.member = tf.DIV("Booked by: ${created_by_name}", Class="member-name")
        bookings_tmpl.aday.bookings.loop_end = "{{/each}}"

        container.resource_pane = resource_pane
        container.booking_pane = booking_pane
        container.bookings_tmpl = bookings_tmpl
        container.script = sphc.more.script_fromfile("fe/src/js/booking_agenda.js")

        return container
