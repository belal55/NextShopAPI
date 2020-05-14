from django.db import models
from .Category import Category

class SubCategory(models.Model):
	category=models.ForeignKey(Category,on_delete=models.SET_NULL,null=True,blank=True)
	name=models.CharField(max_length=100)
	date_created=models.DateTimeField(auto_now_add=True,blank=True,null=True)

	def __str__(self):
		return self.name
