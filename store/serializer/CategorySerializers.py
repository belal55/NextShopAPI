from rest_framework import serializers
from ..model import *
from .SubCategorySerializers import SubCategorySerializer

class CategorySerializer(serializers.ModelSerializer):
	subcategory_set = SubCategorySerializer(many=True,read_only=True)
	class Meta:
		model = Category
		fields = ['id','name','date_created','subcategory_set']
