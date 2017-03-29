from django.db import models
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import User

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
    course_id = models.CharField(unique=True, max_length=12)
    semester = models.CharField()
    year = models.IntegerField()

class Section(models.Model):
    class_day = models.DateField()
    class_time = models.TimeField()
    section_number = models.CharField()
    room_size = models.IntegerField()
    room_number = models.IntegerField()
    router = models.CharField()

class Attendance(models.Model):
    attendance_day = models.DateField()
    time_in = models.TimeField()
    attendance_code = models.CharField()
