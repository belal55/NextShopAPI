from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import viewsets

from ..model import ProductImage
from ..serializer import ProductImageSerializer

class ProductImageViewSet(viewsets.ModelViewSet):
	queryset=ProductImage.objects.all()
	serializer_class=ProductImageSerializer