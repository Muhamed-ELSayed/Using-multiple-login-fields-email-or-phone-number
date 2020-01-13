from django.db import models
from django.utils.translation import gettext as _

# Create your models here.


class Users (models.Model):
    """
    Creat a custom user
    """

    fullname = models.CharField(max_length=255)
    phone_number = models.PositiveIntegerField()
    email = models.EmailField()
    password = models.CharField(max_length=15)
    verfiy_pass = models.CharField(max_length=15)

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def __str__(self):
        return self.fullname

    # def get_absolute_url(self):
    #     return reverse("_detail", kwargs={"pk": self.pk})
