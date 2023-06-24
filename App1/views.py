from django.shortcuts import render
# Create your views here.
from django.http import HttpResponse
from rest_framework import generics, permissions
from rest_framework.response import Response
from knox.models import AuthToken
from .serializers import UserSerializer, RegisterSerializer

#fun1 fun2 fun3 fun4 fun 5 fun 6 are just for understanding, they have no use in the actual proj

def fun1(request):
     return render (request,'HomePage.html')

def fun2(request):
     a=request.GET.get("a")
     b=request.GET.get("b")
     print(a)
     print(b)
     #return render (request,'Form.html')
     return render (request,'Form.html',{'Answer1':a,'Answer2':b})
   # str = "<h1 style = 'color: #663300' >Test Page</h1>"
    #return HttpResponse (str)

def fun3(request):
    return render (request,'About.html')	
    #return render (request,'test.html',{'MyValue':'My Website','MyValue2':'My Website'})

def fun4(request):
    return render (request,'Blogs.html')	

def fun5(request):
    return render (request,'Login.html')

def fun6(request):
    return render (request,'Register.html')




# Register API
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
        "user": UserSerializer(user, context=self.get_serializer_context()).data,
        "token": AuthToken.objects.create(user)[1]
        })
from django.contrib.auth import login

from rest_framework import permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView

#Login API
class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)

