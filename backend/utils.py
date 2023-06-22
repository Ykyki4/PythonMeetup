from django.utils.timezone import localtime, localdate

from .models import User, Event, Question, VisitCard


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
        'date': event.date,
        'time': event.time,
        'speaker': serialize_user(event.speaker),
    }


def serialize_question(question):
    return {
        'guest': serialize_user(question.guest),
        'event': serialize_event(question.event),
        'content': question.content,
    }


def serialize_visit_card(visit_card):
    return {
        'owner': visit_card.owner,
        'first_name': visit_card.first_name,
        'last_name': visit_card.last_name,
        'job_title': visit_card.job_title,
        'phone': visit_card.phone,
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
    events = [serialize_event(event)
              for event in Event.objects.filter(time__gte=localtime(), date__gte=localdate())]
    return events


def get_event(title):
    try:
        event = Event.objects.get(title=title)
        return serialize_event(event)
    except Event.DoesNotExist:
        return None


def create_question(guest, event, content):
    question = Question.objects.create(guest=guest, event=event, content=content)
    return serialize_question(question)


def get_questions(telegram_id):
    speaker = User.objects.get(telegram_id=telegram_id)
    events = speaker.events.all()
    questions = [serialize_question(question) for event in events for question in event.questions.all()]
    return questions


def create_visit_card(telegram_id, first_name, last_name, job_title, phone):
    user = User.objects.get(telegram_id=telegram_id)

    visit_card = VisitCard.objects.create(
        owner=user,
        first_name=first_name,
        last_name=last_name,
        job_title=job_title,
        phone=phone
    )

    return serialize_visit_card(visit_card)
