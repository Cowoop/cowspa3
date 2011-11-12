import be.bootstrap
import be.bootstrap
be.bootstrap.start('conf_test')
import be.apis.plan as planlib
import be.repository.access as dbaccess
dbaccess.get_member_current_subscriptions(1)
planlib.plan_resource.new_member(3, '1.1.2011', 1)
planlib.plan_resource.new_member(4, '1.8.2011', 1)
dbaccess.get_member_subscriptions(1)
