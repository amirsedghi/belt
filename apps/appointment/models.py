from __future__ import unicode_literals

from django.db import models

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    date_of_birth = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now_add = True)

class Appointment(models.Model):
    task = models.CharField(max_length = 255)
    status = models.CharField(max_length = 255, default = 'pending')
    date = models.DateTimeField()
    time = models.TimeField()
    user = models.ForeignKey(User, related_name = 'a_date', on_delete = models.CASCADE)
