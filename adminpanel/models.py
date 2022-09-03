from datetime import datetime
import uuid
from django.db import models
from accounts.models import IcoUser
from django.db.models.signals import post_delete
from django.dispatch.dispatcher import receiver
import os
# Create your models here.


def _delete_file(path):
    # Deletes file from filesystem.
    if os.path.isfile(path):
        os.remove(path)

class Quiz(models.Model):
    name = models.CharField(max_length=25, null=True)
    start_time = models.DateTimeField(null=False)
    end_time = models.DateTimeField(null=False)

    def __str__(self) -> str:
        return self.name

class Participant(models.Model):
    user = models.ForeignKey(IcoUser, null=True, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, null=True,on_delete=models.CASCADE)
    score = models.IntegerField(null=False, blank=False, default=0)
    correct = models.IntegerField(default=0)
    incorrect = models.IntegerField(default=0)
    rank = models.IntegerField(null=True, blank=True,)
    last_visited = models.IntegerField(default=0)
    time_appeared = models.DateTimeField(default=datetime.now(),editable=False)

    class Meta:
        db_table = 'quiz'


ANSWER = (('a','A'), ('b','B'), ('c','C'), ('d','D'))
class Question(models.Model):
    question_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    quiz = models.ForeignKey(Quiz, null=True, on_delete=models.CASCADE, related_name='quiz')
    img = models.ImageField(upload_to="question/", null=True)
    question = models.CharField(max_length=250, null=True, blank=True)
    option_A = models.CharField(max_length=250, null=True, blank=True)
    option_B = models.CharField(max_length=250, null=True, blank=True)
    option_C = models.CharField(max_length=250, null=True, blank=True)
    option_D = models.CharField(max_length=250, null=True, blank=True)
    answer = models.CharField(max_length=1, choices=ANSWER, null=True, blank=True)
    points = models.IntegerField(default=1,null=False)
    time = models.IntegerField(default=1,null=False)
    sequence_no = models.IntegerField(default=1,null=False)
    given_by = models.ForeignKey(IcoUser, on_delete=models.SET_NULL, related_name='author',null=True)

    
    def delete(self):
        self.img.delete()
        super(Question, self).delete()

    class Meta:
        db_table = 'question'


@receiver(post_delete, sender=Question)
def delete_file(sender, instance, *args, **kwargs):
    """ Deletes image files on `post_delete` """
    if instance.img:
        _delete_file(instance.img.path)
