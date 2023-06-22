from django.contrib import admin
from django import forms

from .models import User, Question, Event, VisitCard


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    def render_change_form(self, request, context, *args, **kwargs):
        context['adminform'].form.fields['speaker'].queryset = User.objects.filter(is_speaker=True)
        return super(EventAdmin, self).render_change_form(request, context, args, kwargs)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    pass


@admin.register(VisitCard)
class VisitAdmin(admin.ModelAdmin):
    pass
