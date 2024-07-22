
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class MyUserManager(BaseUserManager):
    def create_user(self, username, password=None):
        if not username:
            raise ValueError("Users must have a username")
        user = self.model(username=username)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None):
        user = self.create_user(username=username, password=password)
        user.is_admin = True
        user.save(using=self._db)
        return user

class MyUser(AbstractBaseUser):
    username = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin
    
class uploaded_data(models.Model):
    UG = 'UG'
    PG = 'PG'
    
    COURSE_CATEGORIES = [
        (UG, 'Undergraduate'),
        (PG, 'Postgraduate')
    ]

    exam_code = models.CharField(max_length=100, null=True)
    student_batch_name = models.CharField(max_length=255, null=True)
    batch_name = models.CharField(max_length=255, null=True)
    class_name = models.CharField(max_length=255, null=True)
    student_name = models.CharField(max_length=255, null=True)
    reg_no = models.CharField(max_length=50, null=True)
    roll_no = models.CharField(max_length=50, null=True)
    exam_type = models.CharField(max_length=100, null=True)
    subject_type = models.CharField(max_length=100, null=True)
    subject_code = models.CharField(max_length=100, null=True)
    subject_name = models.CharField(max_length=255, null=True)
    semester = models.CharField(max_length=50, null=True)
    obt_marks = models.FloatField(null=True)
    max_marks = models.FloatField(null=True)
    obt_grade = models.CharField(max_length=2, null=True)
    is_backlog = models.CharField(max_length=2, null=True)
    is_pass = models.CharField(max_length=2, null=True)
    backlog_attempt_number = models.IntegerField(null=True)
    credit_point_earned = models.FloatField(null=True)
    credit_point_offered = models.FloatField(null=True)
    rv_marks = models.FloatField(null=True)
    rv_updated = models.CharField(max_length=2, null=True)

    # extra columns
    course_category = models.CharField(
        max_length=2,
        choices=COURSE_CATEGORIES
    )
    report_name = models.CharField(max_length=255, null=True)

    def __str__(self):
        return f"{self.report_name} - {self.roll_no} - {self.subject_name}"
