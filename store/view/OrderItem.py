from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import viewsets

from ..model import OrderItem
from ..serializer import OrderItemSerializer

class OrderItemViewSet(viewsets.ModelViewSet):
	queryset=OrderItem.objects.all()
	serializer_class=OrderItemSerializer