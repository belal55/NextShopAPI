from rest_framework import serializers
from ..model import Order,Product,OrderItem

class OrderItemSerializer(serializers.ModelSerializer):
	id = serializers.IntegerField(read_only=False,allow_null=True)
	productName= serializers.CharField(read_only=True, source="product.name")
	photo_url= serializers.SerializerMethodField()

	class Meta:
		model = OrderItem
		fields = ['id','product','productName','photo_url','order','quantity','amount','date_created']
		read_only_fields=['date_created']

	def get_photo_url(self, obj):
		request = self.context.get('request')
		photo_url = obj.product.thumbnail.url
		return request.build_absolute_uri(photo_url)
