from django.contrib import admin

from adminpanel.models import Participant, Question, Quiz

# Register your models here.
admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Participant)