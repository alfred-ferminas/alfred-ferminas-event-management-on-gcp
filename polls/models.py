import datetime
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text

class usermails(models.Model):
    email = models.EmailField(max_length=254,default="")
    subject = models.CharField(max_length=100,default="")
    message = models.TextField(max_length=1000,default="")

    def __str__(self):
        return self.subject

class registeredevents(models.Model):
    eventid = models.AutoField(primary_key = True)
    eventname = models.CharField(default="",max_length=100)
    purpose = models.TextField(default="", max_length=1000)
    location = models.CharField(default="",max_length=100)
    date = models.DateField(auto_now=False, auto_now_add=False)
    type = models.CharField(max_length=50)
    username = models.CharField(max_length = 50, default = "")
    # document = models.FileField(_(""), upload_to=None, max_length=100)

    def __str__(self):
        return self.eventname

class notification(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.TextField(max_length = 1000, default = "")
    datetime = models.DateTimeField(auto_now_add=True)
    username = models.CharField(max_length = 50, default = "")
    def __str__(self):
        return self.description

class registration(models.Model):
    id = models.AutoField(primary_key=True)
    eventid = models.ForeignKey(registeredevents, on_delete=models.CASCADE,default="")
    username = models.ForeignKey(User, on_delete=models.CASCADE,default="")

    def __str__(self):
        return str(self.id)