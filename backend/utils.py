from .models import User, Event, Question


def serialize_user(user):
    return {
        'telegram_id': user.telegram_id,
        'name': user.name,
        'about': user.about,
        'is_speaker': user.is_speaker,
    }


def serialize_event(event):
    return {
        'title': event.title,
        'description': event.description,
        'time': event.time,
        'speaker': serialize_user(event.speaker),
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


def get_events():
    events = [serialize_event(event) for event in Event.objects.all()]
    return events
