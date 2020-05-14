from django.db import models
from .Order import Order
from .Product import Product

class OrderItem(models.Model):
	order=models.ForeignKey(Order,on_delete=models.CASCADE,null=True,blank=True)
	product=models.ForeignKey(Product,on_delete=models.SET_NULL,null=True,blank=True)
	quantity=models.IntegerField()
	amount=models.FloatField()
	date_created=models.DateTimeField(auto_now_add=True,blank=True,null=True)

	def __str__(self):
		return self.product.name
