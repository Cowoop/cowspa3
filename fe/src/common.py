import sphc
import commonlib.shared.static as data_lists

tf = sphc.TagFactory()

country_options =  [ tf.OPTION(country['label'], value=country['name']) for country in data_lists.countries ]
