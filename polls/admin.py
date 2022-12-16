from django.contrib import admin
from .models import Question, Choice, User


class ChoiceInLine(admin.TabularInline):
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInLine]


admin.site.register(Question, QuestionAdmin)
admin.site.register(User)