from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from account.permissions import IsLoggedInUserOrAdmin, IsAdminUser

from ..model import *
from ..serializer import ProductSerializer

class ProductViewSet(viewsets.ModelViewSet):
	queryset=Product.objects.all()
	serializer_class=ProductSerializer

	def get_permissions(self):
		permission_classes = []
		if self.action == 'create' or self.action == 'destroy':
			permission_classes = [IsAdminUser]
		elif self.action == 'retrieve' or self.action == 'update' or self.action == 'partial_update':
			permission_classes = [IsAdminUser]
		elif self.action == 'list':
			permission_classes = [AllowAny]
		return [permission() for permission in permission_classes]