from rest_framework import serializers
from ..model import ProductImage,Product

class ProductImageSerializer(serializers.ModelSerializer):
	id = serializers.IntegerField(read_only=False,allow_null=True)
	productName= serializers.CharField(read_only=True, source="product.name")
	class Meta:
		model = ProductImage
		fields = ['id','image','date_created','product','productName']