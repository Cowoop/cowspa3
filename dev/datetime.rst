Date/datetime
=======================================

communication guidelines
------------------------

 - Backend APIs would always accept date and datetime in ISO 8601 format strings
 - Backend APIs would not accept native python datetime objects
 - Frontend would show dates in readable format like "Jan 5, 2011". These are visible fields and only purpose is to show date in readable format to user.
 - Frontend would have hidden date/datetime fields (alt field) which is real datetime input field and will hold the value to sent to Backend

Notes
-----

 - native (html5) date/datetime fields do not support alt formats
 - timepicker plugin does not support alt formats either
