from django.contrib import admin
from .models import User, Question, Event, VisitCard


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    pass


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    pass


@admin.register(VisitCard)
class QuestionAdmin(admin.ModelAdmin):
    pass
