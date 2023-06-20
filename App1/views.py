from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse


from rest_framework import generics, permissions
from rest_framework.response import Response
from knox.models import AuthToken
from .serializers import UserSerializer, RegisterSerializer

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

class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)

def fun1(request): #eXTRA
    print("INSIDE HOME PAGWE")
    return render (request,'HomePage.html')

def fun2(request): #eXTRA
     a=5
     b=6
     #return render (request,'Form.html')
     return render (request,'Form.html',{'Answer1':a,'Answer2':b})


   # str = "<h1 style = 'color: #663300' >Test Page</h1>"
    #return HttpResponse (str)

def fun3(request):#eXTRA
    return render (request,'About.html')	
    #return render (request,'test.html',{'MyValue':'My Website','MyValue2':'My Website'})

def fun4(request):#eXTRA
    return render (request,'Blogs.html')	

def fun5(request):#eXTRA
    return render (request,'Login.html')

def fun6(request): #eXTRA
    return render (request,'Register.html')




from rest_framework import permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LogoutView as KnoxLogoutView

# class LogoutAPI(KnoxLogoutView):
#     permission_classes = (permissions.AllowAny,)

#     def post(self, request, format=None):
#         serializer = AuthTokenSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data['user']
#         logout(request, user)
#         return super(LogoutAPI, self).post(request, format=None)







# # django imports
# from django.contrib.auth import login

# # rest_framework imports
# from rest_framework import generics, authentication, permissions
# from rest_framework.settings import api_settings
# from rest_framework.authtoken.serializers import AuthTokenSerializer

# # knox imports
# from knox.views import LoginView as KnoxLoginView
# from knox.auth import TokenAuthentication

# # local apps import
# from core.serializers import UserSerializer, AuthSerializer

# from rest_framework.authentication import SessionAuthentication



# class CreateUserView(generics.CreateAPIView):
#     # Create user API view
#     serializer_class = UserSerializer


# class LoginView(KnoxLoginView):
#     # login view extending KnoxLoginView
#     serializer_class = AuthSerializer
#     permission_classes = (permissions.AllowAny,)

#     def post(self, request, format=None):
#         serializer = AuthTokenSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data['user']
#         login(request, user)
#         return super(LoginView, self).post(request, format=None)    


# class ManageUserView(generics.RetrieveUpdateAPIView):
#     """Manage the authenticated user"""
#     serializer_class = UserSerializer
#     permission_classes = (permissions.IsAuthenticated,)

#     def get_object(self):
#         """Retrieve and return authenticated user"""
#         return self.request.user