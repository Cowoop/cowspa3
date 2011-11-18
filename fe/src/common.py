import sphc
import commonlib.shared.static as data_lists
from commonlib.shared.roles import team_roles

tf = sphc.TagFactory()

country_options =  [ tf.OPTION(country['label'], value=country['name']) for country in data_lists.countries ]
team_options =  [ tf.INPUT(role.label, type="checkbox", name="roles", value=role.name) for role in team_roles]
#tz_options =  [ tf.OPTION(tz['label'], value=tz['name']) for tz in
#        data_lists.timezones ]
