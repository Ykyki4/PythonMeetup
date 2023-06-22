from .models import User, Event, Question


def serialize_user(user):
    return {
        'telegram_id': user.telegram_id,
        'name': user.name,
        'is_speaker': user.is_speaker,
    }


def serialize_event(event):
    return {
        'title': event.title,
        'description': event.description,
        'time': event.time,
        'speaker': serialize_user(event.speaker),
    }


def serialize_question(question):
    return {
        'guest': serialize_user(question.guest),
        'event': serialize_event(question.event),
        'content': question.content,
    }


def create_user(telegram_id, name):
    user = User.objects.create(telegram_id=telegram_id, name=name)
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


def create_question(guest, event, content):
    question = Question.objects.create(guest=guest, event=event, content=content)
    return serialize_question(question)


def get_questions(telegram_id):
    speaker = User.objects.get(telegram_id=telegram_id)
    events = speaker.events.all()
    questions = [serialize_question(question) for event in events for question in event.questions.all()]
    return questions
