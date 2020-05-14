from django.db import models
from .Product import Product
from django.db.models.signals import post_delete,pre_save
from django.dispatch import receiver

class ProductImage(models.Model):
	product=models.ForeignKey(Product,on_delete=models.CASCADE,null=True,blank=True)
	image=models.ImageField(null=True,blank=True)
	date_created=models.DateTimeField(auto_now_add=True,blank=True,null=True)

	def __str__(self):
		return self.product.name

@receiver(post_delete, sender=ProductImage)
def submission_delete(sender, instance, **kwargs):
	instance.image.delete(False)
