from django.db import models
import datetime
from django.contrib.auth.models import User
from account.models import Address
from django.conf import settings

class Order(models.Model):
	user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True)
	address=models.ForeignKey(Address,on_delete=models.SET_NULL,null=True,blank=True)
	transactionId=models.CharField(max_length=100,unique=True)
	status=models.CharField(max_length=20,choices=[
		('PROCESSING','PROCESSING'),
		('PREPERING','PREPERING'),
		('SHIPPING','SHIPPING'),
		('DELIVERED','DELIVERED'),
		('CANCELED','CANCELED'),
		('PENDING','PENDING'),
	])
	date_created=models.DateTimeField(auto_now_add=True,blank=True,null=True)

	def __str__(self):
		return self.transactionId
