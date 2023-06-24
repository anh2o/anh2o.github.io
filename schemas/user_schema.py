
def user_serializer(user) -> dict:
    return {
        'id':str(user["_id"]),
        'name':user["name"],
        'tgid':user["tgid"],
        'pay_state':user["pay_state"],
    }

def users_serializer(users) -> list:
    return [user_serializer(user) for user in users]