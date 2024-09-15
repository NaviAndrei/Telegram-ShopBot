from credentials import admin_user_ids


def is_admin(user_id):
    return user_id in admin_user_ids
