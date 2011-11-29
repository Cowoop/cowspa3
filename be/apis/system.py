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
    data = dict(username=username, password=password, email=email, first_name=first_name)
    admin_user_id = memberlib.member_collection.new(**data)
    rolelib.new_roles(admin_user_id, ['admin'], 0)
    return (system_user_id, admin_user_id)
