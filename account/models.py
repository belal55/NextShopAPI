from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.conf import settings


class User(AbstractUser):
	username = models.CharField(max_length=10,blank=True,null=True)
	email = models.EmailField(_('email address'),unique=True)

	USERNAME_FIELD= 'email'
	REQUIRED_FIELDS=['username','first_name','last_name']

	def __str__(self):
		return self.email



class UserProfile(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,
	related_name='profile',blank=True,null=True)
	mobileNo = models.CharField(max_length=15,blank=True,null=True)
	image = models.ImageField(blank=True,null=True)


class Address(models.Model):
	user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,null=True,blank=True)
	title = models.CharField(max_length=100,blank=True,null=True)
	date_created = models.DateField(null=True, blank=True)

	def __str__(self):
		return self.title + ' ('+self.user.email+')'
