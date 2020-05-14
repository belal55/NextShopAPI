from django.db import models

class Brand(models.Model):
	name=models.CharField(max_length=100)
	date_created=models.DateTimeField(auto_now_add=True,blank=True,null=True)

	def __str__(self):
		return self.name