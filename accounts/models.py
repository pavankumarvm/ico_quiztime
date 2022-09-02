import uuid
from django.db import models

from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin

from .managers import UserManager
import uuid
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch.dispatcher import receiver
import os

# Create your models here.

def _delete_file(path):
    # Deletes file from filesystem.
    if os.path.isfile(path):
        os.remove(path)

class IcoUser(AbstractBaseUser, PermissionsMixin):

    # Creates User
    user_id = models.UUIDField(primary_key=True, default = uuid.uuid4, editable=False)
    username = models.CharField(max_length=25, unique=True, null=False)
    avatar = models.ImageField(upload_to="profile/", null=True)
    first_name = models.CharField(max_length=30, blank=False, null=True)
    last_name = models.CharField(max_length=30, blank=False, null=True)
    email = models.EmailField(max_length=50, blank=False, null=False, unique=True)
    phone_no = models.CharField(max_length=10, blank=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last login", auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    age = models.CharField(max_length=4,null=True)
    gender = models.CharField(max_length=1,null=True)
    total_score = models.BigIntegerField(default=0)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return f'{self.username}'

    def has_perm(self, perm, obj=None):
        return self.is_staff

    def has_module_perms(self, app_label):
        return True

    def delete(self):
        self.avatar.delete()
        super(IcoUser, self).delete()


    class Meta:
        db_table = 'ico_user'


@receiver(post_delete, sender=IcoUser)
def delete_file(sender, instance, *args, **kwargs):
    """ Deletes image files on `post_delete` """
    if instance.avatar:
        _delete_file(instance.avatar.path)


class Otp(models.Model):
    user = models.OneToOneField(IcoUser, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    otp_valid_time = models.DateTimeField(auto_now_add=True)
    no_of_attempts = models.IntegerField(default = 5)

    class Meta:
        db_table = "otp"
    