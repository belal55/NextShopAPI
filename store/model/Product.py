from django.db import models
from .Category import Category
from .SubCategory import SubCategory
from .Brand import Brand

from django.db.models.signals import post_delete,pre_save
from django.dispatch import receiver

class Product(models.Model):
	category=models.ForeignKey(Category,on_delete=models.SET_NULL,null=True,blank=True)
	subCategory=models.ForeignKey(SubCategory,on_delete=models.SET_NULL,null=True,blank=True)
	brand=models.ForeignKey(Brand,on_delete=models.SET_NULL,null=True,blank=True)
	name=models.CharField(max_length=250)
	thumbnail=models.ImageField(blank=True,null=True)
	price=models.FloatField()
	stock=models.FloatField()
	description=models.TextField(blank=True,null=True)
	specification=models.TextField(blank=True,null=True)
	policy=models.TextField(blank=True,null=True)
	viewCount=models.IntegerField(default=0)
	isUpComing=models.BooleanField(default=False,blank=True,null=True)
	isFeatured=models.BooleanField(default=False,blank=True,null=True)
	isActive=models.BooleanField(default=False,blank=True,null=True)
	date_created=models.DateTimeField(auto_now_add=True,blank=True,null=True)

	def __str__(self):
		return self.name

@receiver(post_delete, sender=Product)
def submission_delete(sender, instance, **kwargs):
	instance.thumbnail.delete(False)

# @receiver(pre_save, sender=Product)
# def submission_delete(sender, instance, **kwargs):
# 	instance.productimage_set.all().delete()