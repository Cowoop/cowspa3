import be.apis.role as rolelib
import be.apis.user as userlib
import be.apis.member as memberlib
import be.repository.access as dbaccess

def setup(username, password, email, first_name):
    if dbaccess.stores.user_store.count():
        return
    # 1. Create system account
    system_user_id = userlib.create_system_account()
    # 2. Create an Admin member
    admin_user_id = memberlib.member_collection.new(username, password, email, first_name)
    rolelib.assign(admin_user_id, ['admin'])
    return (system_user_id, admin_user_id)
