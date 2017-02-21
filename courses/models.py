from django.db import models
from django.contrib.auth.models import User


class Course(models.Model):
    course_code = models.CharField()
    semester = models.CharField()
    room_number = models.IntegerField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    SSID = models.CharField()
