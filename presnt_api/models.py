from django.db import models
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import User
from datetime import datetime

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    pid = models.CharField(
        max_length=7,
        validators=[MinLengthValidator(7)],
        unique=True,
    )
    is_professor = models.BooleanField(default=False)
    profile_image = models.ImageField(blank=True)

    def has_professor_permissions(self):
        if self.is_professor:
            return True
        else:
            return False

class Course(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    course_name = models.CharField(max_length=32)
    course_id = models.CharField(unique=True, max_length=12)
    semester = models.CharField(max_length=16)

class Section(models.Model):
    professor = models.ForeignKey(
            User,
            on_delete=models.CASCADE,
            related_name='professor',
    )
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    class_day_one = models.CharField(max_length=32)
    class_day_two = models.CharField(
            max_length=32,
            blank=True,
    )
    class_day_three = models.CharField(
            max_length=32,
            blank=True,
    )
    class_time = models.TimeField()
    room_size = models.IntegerField()
    room_number = models.IntegerField()
    roster = models.ManyToManyField(
            User,
            related_name='roster',
            blank=True,
    )
    router = models.CharField(max_length=32)
    section_id = models.CharField(max_length=32)

class Attendance(models.Model):
    student = models.ForeignKey(
            User,
            on_delete=models.CASCADE,
            related_name='student'
    )
    section = models.ForeignKey(
            Section,
            on_delete=models.CASCADE,
            related_name='section'
    )
    attendance_day = models.DateField()
    time_in = models.TimeField(auto_now_add=True)
