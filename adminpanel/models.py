import uuid
from django.db import models
from accounts.models import IcoUser, Participant
# Create your models here.

ANSWER = (('a','A'), ('b','B'), ('c','C'), ('d','D'))
class Question(models.Model):
    question_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    category = models.CharField(max_length=50, null=True, blank=True)
    question = models.CharField(max_length=250, null=False, blank=False)
    option_A = models.CharField(max_length=250, null=True, blank=True)
    option_B = models.CharField(max_length=250, null=True, blank=True)
    option_C = models.CharField(max_length=250, null=True, blank=True)
    option_D = models.CharField(max_length=250, null=True, blank=True)
    answer = models.CharField(max_length=1, choices=ANSWER, null=True, blank=True)
    explanation = models.CharField(max_length=250, null=True, blank=True)
    given_by = models.ForeignKey(IcoUser, on_delete=models.SET_NULL, related_name='author',null=True)

    class Meta:
        db_table = 'question'

class Quiz(models.Model):
    name = models.CharField(max_length=25, null=True)
    start_time = models.DateTimeField(null=False)
    end_time = models.DateTimeField(null=False)
    participant = models.ForeignKey(to=Participant,on_delete=models.CASCADE, null=True)
