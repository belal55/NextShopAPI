from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
import json
from rest_framework_simplejwt.tokens import RefreshToken

from account.models import User,Address
from store.model import Order
from account.serializers import UserSerializer,RegistrationSerializer
# Also add these imports
from account.permissions import IsLoggedInUserOrAdmin, IsAdminUser,IsLogged

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    # Add this code block
    def get_permissions(self):
        permission_classes = []
        if self.action == 'create':
            permission_classes = [AllowAny]
        elif self.action == 'retrieve' or self.action == 'update' or self.action == 'partial_update':
            permission_classes = [IsLoggedInUserOrAdmin]
        elif self.action == 'list' or self.action == 'destroy':
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]


@api_view(['POST'])
def menual_token(request):
    order=Order.objects.get(transactionId=request.data['transactionId'])
    user=User.objects.get(id=order.user.id)
    refresh = RefreshToken.for_user(user)
    # Add custom claims
    refresh['email'] = user.email
    refresh['groups'] = user.groups.values_list('name', flat=True)[0]

    context={'refresh': str(refresh),'access': str(refresh.access_token)}
    return Response(context,status=status.HTTP_200_OK)


@api_view(['POST'])
def check_email(request):
    try:
        user=User.objects.get(email=request.data['email'])
        address=user.address_set.all()
        if(address):
            address=address.latest('id')
            context={"id":user.id,'address':address.title,'addressId':address.id}
        else:
            context={"id":user.id,'address':'','addressId':None}

        return Response(context,status=status.HTTP_200_OK)
    except:
        context={"id":None,'address':'','addressId':None}
        return Response(context,status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes((IsLogged, ))
def configure_pass(request):
    try:
        user=User.objects.get(email=request.data['email'])
        group=user.groups.values_list('name', flat=True)[0]
        if(group=='Customer'):
            user.set_password(request.data['password'])
            user.save()
            context={"success":True}
            return Response(context,status=status.HTTP_200_OK)
        else:
            context={"success":False}
            return Response(context,status=status.HTTP_200_OK)
    except:
        context={"success":False}
        return Response(context,status=status.HTTP_200_OK)

@api_view(['POST'])
def regiUser(request):
	serializer=RegistrationSerializer(data=request.data)
	if serializer.is_valid():
		serializer.save()
		return Response(serializer.data)
	return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['email'] = user.email
        token['groups'] = user.groups.values_list('name', flat=True)[0]
        # ...

        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        # Add extra responses here
        data['email'] = self.user.email
        data['groups'] = self.user.groups.values_list('name', flat=True)
        return data


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer