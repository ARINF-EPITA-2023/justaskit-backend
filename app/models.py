from datetime import datetime

from django.db import models


class Question(models.Model):
    question_text = models.CharField(max_length=500)
    pub_date = models.DateTimeField('date published', default=datetime.now)
    response1 = models.ForeignKey('Response', on_delete=models.CASCADE, related_name='response1')
    response2 = models.ForeignKey('Response', on_delete=models.CASCADE, related_name='response2')
    upvotes = models.IntegerField(default=0)
    downvotes = models.IntegerField(default=0)

    def __str__(self):
        return self.question_text


class Response(models.Model):
    response_text = models.CharField(max_length=500)
    choices = models.IntegerField(default=0)

    def __str__(self):
        return self.response_text
