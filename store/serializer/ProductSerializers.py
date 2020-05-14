from rest_framework import serializers
from ..model import *
from .ProductImageSerializers import ProductImageSerializer

class ProductSerializer(serializers.ModelSerializer):
	categoryName= serializers.CharField(read_only=True, source="category.name")
	subCategoryName= serializers.CharField(read_only=True, source="subCategory.name")
	brandName= serializers.CharField(read_only=True, source="brand.name")
	productimage_set = ProductImageSerializer(many=True,required=False)

	def create(self, validated_data):
		image_data = self.initial_data.getlist('productimage_set[]')
		product = Product.objects.create(**validated_data)
		for item_data in image_data:
			item_data.product=product
			ProductImage.objects.create(product=product, image=item_data)
		return product


	def update(self, instance, validated_data):
		instance.name = validated_data.get('name', instance.name)
		instance.price=validated_data.get('price', instance.price)
		instance.stock=validated_data.get('stock', instance.stock)
		instance.thumbnail=validated_data.get('thumbnail', instance.thumbnail)
		instance.description=validated_data.get('description', instance.description)
		instance.specification=validated_data.get('specification', instance.specification)
		instance.policy=validated_data.get('policy', instance.policy)
		instance.isUpComing=validated_data.get('isUpComing', instance.isUpComing)
		instance.isFeatured=validated_data.get('isFeatured', instance.isFeatured)
		instance.isActive=validated_data.get('isActive', instance.isActive)
		instance.category=validated_data.get('category', instance.category)
		instance.subCategory=validated_data.get('subCategory', instance.subCategory)
		instance.brand=validated_data.get('brand', instance.brand)
		instance.save()

		
		items = self.initial_data.getlist('productimage_set[]')
		for item in items:
			ProductImage.objects.create(product=instance,image=item)

		return instance


	class Meta:
		model = Product
		fields = ['id','name','thumbnail','price','stock','description','specification','policy',
				'viewCount','isUpComing','isFeatured','isActive','date_created',
				'category','categoryName','subCategory','subCategoryName','brand','brandName','productimage_set']