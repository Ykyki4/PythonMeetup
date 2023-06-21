from .models import User


def serialize_user(user):
    return {
        'telegram_id': user.telegram_id,
        'name': user.name,
        'about': user.about,
    }


def create_user(telegram_id, name, about=None):
    user = User.objects.create(telegram_id=telegram_id, name=name, about=about)
    return serialize_user(user)


def get_user(telegram_id):
    try:
        user = User.objects.get(telegram_id=telegram_id)
        return serialize_user(user)
    except User.DoesNotExist:
        return None
