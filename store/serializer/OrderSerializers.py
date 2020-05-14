from rest_framework import serializers
from ..model import Order,OrderItem
import datetime
from .OrderItemSerializers import OrderItemSerializer
from django.db.models import Avg, Max, Min, Sum
from account.serializers import RegistrationSerializer
from account.models import User,Address


class OrderSerializer(serializers.ModelSerializer):
	email= serializers.CharField(read_only=True, source="user.email")
	shippingAddress= serializers.CharField(read_only=True, source="address.title")
	orderitem_set = OrderItemSerializer(many=True)
	sub_total=serializers.SerializerMethodField()
	total_quantity=serializers.SerializerMethodField()

	def get_sub_total(self,obj):
		sub_total=obj.orderitem_set.aggregate(Sum('amount'))['amount__sum']
		return sub_total

	def get_total_quantity(self,obj):
		sub_total=obj.orderitem_set.aggregate(Sum('quantity'))['quantity__sum']
		return sub_total

	def create(self, validated_data):

		if self.initial_data.get('newEmail'):
			mail=self.initial_data.get('newEmail')
			rpass=User.objects.make_random_password()
			usr={"email":mail,"password":rpass}
			regSerializer=RegistrationSerializer(data=usr)

			if(regSerializer.is_valid()):
				regSerializer.save()
				newUser=User.objects.get(id=regSerializer.data['id'])
				validated_data['user']=newUser
				add=Address.objects.create(user=newUser,title=self.initial_data.get('newAddress'))
				validated_data['address']=add


		if self.initial_data.get('user') and self.initial_data.get('newAddress'):
			anotherAdd=Address.objects.create(user=validated_data['user'],title=self.initial_data.get('newAddress'))
			validated_data['address']=anotherAdd


		orderItems_data = validated_data.pop('orderitem_set')
		validated_data['transactionId'] =(datetime.datetime.now().timestamp()).__str__().replace('.','')
		order = Order.objects.create(**validated_data)

		for item_data in orderItems_data:
			item_data.order=order
			OrderItem.objects.create(order=order, **item_data)

		return order

	def update(self, instance, validated_data):
		instance.status = validated_data.get('status', instance.status)
		instance.address=validated_data.get('address', instance.address)
		instance.save()
		items = validated_data.get('orderitem_set')
		for item in items:
			item_id = item.get('id', None)
			if item_id:
				order_item=OrderItem.objects.get(id=item_id,order=instance)
				order_item.quantity = item.get('quantity', order_item.quantity)
				order_item.amount = item.get('amount', order_item.amount)
				order_item.save()
			else:
				OrderItem.objects.create(**item)

		return instance

	class Meta:
		model = Order
		fields = ['id','transactionId','sub_total','total_quantity','user','email','address','shippingAddress','status','date_created','orderitem_set']
		read_only_fields=['transactionId','date_created']

