from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK,HTTP_204_NO_CONTENT
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from account.permissions import IsLoggedInUserOrAdmin, IsAdminUser

from ..model import Order
from account.models import User
from ..serializer import OrderSerializer

class OrderViewSet(viewsets.ModelViewSet):
	queryset=Order.objects.all()
	serializer_class=OrderSerializer

	def get_permissions(self):
		permission_classes = []
		if self.action == 'create' or self.action == 'destroy' or self.action == 'partial_update':
			permission_classes = [IsLoggedInUserOrAdmin]
		elif self.action == 'retrieve' or self.action == 'update':
			permission_classes = [AllowAny]
		elif self.action == 'list':
			permission_classes = [AllowAny]
		return [permission() for permission in permission_classes]

	@action(detail=True, methods=['post'])
	def update_status(self, request, pk):
		order=self.get_object()
		order.status=request.data['status']
		order.save()
		return Response(OrderSerializer(order).data)

@api_view(['GET'])
def order_by_user(request, id):
	user=User.objects.get(id=id)
	order=Order.objects.filter(user=user)
	return Response(OrderSerializer(order,many=True,context={"request": request}).data,HTTP_200_OK)
