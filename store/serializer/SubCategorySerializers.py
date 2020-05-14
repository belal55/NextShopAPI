from rest_framework import serializers
from ..model import Category,SubCategory

class SubCategorySerializer(serializers.ModelSerializer):
	categoryName= serializers.CharField(read_only=True, source="category.name")
	class Meta:
		model = SubCategory
		fields = ['id','name','date_created','category','categoryName']