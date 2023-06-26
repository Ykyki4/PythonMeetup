from django.utils.timezone import localtime, localdate

from .models import User, Event, Question, VisitCard, Meetup


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


def serialize_visit_card(visit_card):
    return {
        'owner': visit_card.owner,
        'first_name': visit_card.first_name,
        'last_name': visit_card.last_name,
        'job_title': visit_card.job_title,
        'phone': visit_card.phone,
    }


def serialize_meetup(meetup):
    return {
        'title': meetup.title,
        'date': meetup.date,
        'events': [serialize_event(event) for event in meetup.events.all()]
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


def get_today_meetup():
    try:
        meetup = Meetup.objects.get(date=localdate())
        return serialize_meetup(meetup)
    except Meetup.DoesNotExist:
        return None


def get_event(title):
    try:
        event = Event.objects.get(title=title)
        return serialize_event(event)
    except Event.DoesNotExist:
        return None


def get_current_event():
    try:
        meetup = Meetup.objects.get(date=localdate())
        current_event = meetup.events.filter(time__lte=localtime()).last()
        if not current_event:
            return None
        return serialize_event(current_event)
    except Meetup.DoesNotExist:
        return None


def create_question(telegram_id, event_title, content):
    guest = User.objects.get(telegram_id=telegram_id)
    event = Event.objects.get(title=event_title)
    question = Question.objects.create(guest=guest, event=event, content=content)
    return serialize_question(question)


def get_to_speaker_questions(telegram_id):
    try:
        speaker = User.objects.get(telegram_id=telegram_id)
    except User.DoesNotExist:
        return None
    events = speaker.events.all()
    questions = [serialize_question(question) for event in events for question in event.questions.all()]
    return questions


def get_from_guest_questions(telegram_id):
    try:
        guest = User.objects.get(telegram_id=telegram_id)
    except User.DoesNotExist:
        return None
    questions = [serialize_question(question) for question in guest.questions.all()]
    return questions


def get_visit_card(telegram_id):
    try:
        user = User.objects.get(telegram_id=telegram_id)
        visit_card = VisitCard.objects.get(owner=user)
        return serialize_visit_card(visit_card)
    except (User.DoesNotExist, VisitCard.DoesNotExist):
        return None


def create_visit_card(telegram_id, first_name, last_name, job_title, phone):
    try:
        user = User.objects.get(telegram_id=telegram_id)
        VisitCard.objects.get(owner=user).delete()
    except User.DoesNotExist:
        return None
    except VisitCard.DoesNotExist:
        pass

    visit_card = VisitCard.objects.create(
        owner=user,
        first_name=first_name,
        last_name=last_name,
        job_title=job_title,
        phone=phone
    )

    return serialize_visit_card(visit_card)


def get_visit_cards(telegram_id):
    try:
        user = User.objects.get(telegram_id=telegram_id)
    except User.DoesNotExist:
        return None
    visit_cards = [serialize_visit_card(visit_card) for visit_card in VisitCard.objects.exclude(owner=user)]
    return visit_cards
