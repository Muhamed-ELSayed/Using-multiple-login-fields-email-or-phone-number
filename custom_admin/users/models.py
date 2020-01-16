from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.

class UserManager(BaseUserManager):
    # create user and save it
    def create_user(self, phone, email, password=None,):
        if not email:
            raise ValueError('User should be have an email ')

        if not phone:
            raise ValueError('User should be have phone number')

        user = self.model(
            email = self.normalize_email(email),
            phone = phone
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, phone,email, password):
        user = self.create_user(
            email,
            phone,
            password= password
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, phone, password):
        user = self.create_user(
            email,
            phone,
            password= password
        )
        user.staff = True
        user.admin= True
        user.save(using=self._db)
        return user 



# create custom user class
class User(AbstractBaseUser):
    """
    create a custom user model with external class contains all info for the user
    """
    fullname            = models.CharField(max_length=50, verbose_name='Fullname')
    phone               = PhoneNumberField(region="SA", unique=True)
    email               = models.EmailField(max_length=254, unique=True, verbose_name='Email')
    phone_email         = models.CharField(max_length=255, unique=True)
    active              = models.BooleanField(default=True)
    staff               = models.BooleanField(default=False)
    admin               = models.BooleanField(default=False)
    password            = models.CharField(max_length=15, verbose_name='Password')
    password_confirm    = models.CharField(max_length=15)
    objects              = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS=['phone']

    def __str__(self):
        return self.email

    def get_fullname(self):
        if self.fullname:
            return self.fullname
        return self.email

    def get_short_name(self):
        if self.fullname:
            # fn = self.fullname.split( )
            # return fn[0]
            return self.fullname
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_active(self):
        return self.active

    @property
    def is_admin(self):
        return self.admin
    

