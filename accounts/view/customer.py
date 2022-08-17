from rest_framework import status, generics
from rest_framework import permissions
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from accounts.models import User
from rest_framework import pagination
from accounts.serializers import (
    SignupSerializer, LoginSerializer,
    ListSerializer, UpdateDeleteUserSerializer,
)


class DynamicPagination(pagination.PageNumberPagination):
    page_size = 10


class SignUpCustomer(generics.CreateAPIView):
    serializer_class = SignupSerializer
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    pagination_class = DynamicPagination

    def post(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data)
            if not serializer.is_valid():
                return Response({
                    "success": False,
                    "message": serializer.errors,
                    "data": []
                }, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            serializer.instance.is_customer = True
            serializer.instance.save()
            return Response({
                "success": True,
                "message": "User Created Successfully",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "success": False,
                "message": e.args[0],
                "data": []
            }, status=status.HTTP_400_BAD_REQUEST)


class LoginUser(TokenObtainPairView):
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]


    def post(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data)
            if not serializer.is_valid():
                return Response({
                    "success": False,
                    "message": serializer.errors,
                    "data": []
                }, status=status.HTTP_400_BAD_REQUEST)
            user = authenticate(email=serializer.data.get("email"), password=request.data.get("password"))

            if user is not None:
                if user.is_customer and not user.is_superuser:
                    return Response({
                        "success": True,
                        "message": "Customer Login Successfully",
                        "Customer": serializer.user.is_customer,
                        "Admin": serializer.user.is_superuser,
                        "refresh_token": str(RefreshToken.for_user(user)),
                        "access_token": str(AccessToken.for_user(user)),
                        "data": serializer.data
                    }, status=status.HTTP_200_OK)
                elif user.is_superuser:
                    return Response({
                        "success": True,
                        "message": "Admin Login Successfully",
                        "Customer": serializer.user.is_customer,
                        "Admin": serializer.user.is_superuser,
                        "refresh_token": str(RefreshToken.for_user(user)),
                        "access_token": str(AccessToken.for_user(user)),
                        "data": serializer.data
                    }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "success": False,
                "message": e.args[0],
                "data": []
            }, status=status.HTTP_400_BAD_REQUEST)


class ListUser(generics.ListAPIView):
    serializer_class = ListSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = User.objects.all()
    pagination_class = DynamicPagination

    def get(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(self.get_queryset(), many=True)
            return Response({
                "success": True,
                "message": "Customer Data Listed Successfully",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "success": True,
                "message": e.args[0],
                "data": []
            }, status=status.HTTP_400_BAD_REQUEST)


class UpdateDeleteUser(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UpdateDeleteUserSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = User.objects.all()
    pagination_class = DynamicPagination

    def delete(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data, partial=True)
            if not serializer.is_valid():
                return Response({
                    "success": False,
                    "message": serializer.errors,
                    "data": ""
                }, status=status.HTTP_400_BAD_REQUEST)
            user_id = serializer.validated_data['user_id']
            user = self.get_queryset().filter(id=user_id)
            if user.exists():
                user.delete()
                return Response({
                    "success": True,
                    "message": "User Deleted Successfully",
                    "data": None
                }, status=status.HTTP_200_OK)
            return Response({
                "success": False,
                "message": "User Not Found!",
                "data": ""
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                "success": False,
                "message": str(e),
                "data": ""
            }, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data, partial=True)
            if not serializer.is_valid():
                return Response({
                    "success": False,
                    "message": serializer.errors,
                    "data": ""
                }, status=status.HTTP_400_BAD_REQUEST)
            id = self.request.query_params.get('user_id', None)
            user = self.get_queryset().filter(id=id)
            if user.exists():
                user.update()
                serializer = self.get_serializer(user)
                return Response({
                    "success": True,
                    "message": "User Updated Successfully",
                    "data": serializer.data
                }, status=status.HTTP_200_OK)
            return Response({
                "success": False,
                "message": "User Not Found!",
                "data": ""
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                "success": False,
                "message": e.args[0],
                "data": ""
            }, status=status.HTTP_400_BAD_REQUEST)
