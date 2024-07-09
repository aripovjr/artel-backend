from django.shortcuts import render, get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from .models import CustomUser
from .serializers import AccountSerializer, UserSerializer
from rest_framework.pagination import PageNumberPagination


class UserPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 100


class AccountCheckerByID(generics.GenericAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = AccountSerializer

    def get(self, request, *args, **kwargs):
        # Check for telegram_id in both the request body and query parameters
        telegram_id = request.data.get("telegram_id") or request.query_params.get("telegram_id")

        if telegram_id is None:
            return Response({'detail': 'telegram_id is required'}, status=400)

        user = get_object_or_404(CustomUser, telegram_id=telegram_id)
        serializer = self.get_serializer(user)
        return Response(serializer.data)


class AccountCheckerByPhoneNumber(generics.GenericAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = AccountSerializer

    def get(self, request, *args, **kwargs):
        phone_number = request.POST.get("phone_number")
        user = get_object_or_404(CustomUser, phone_number=phone_number)
        serializer = self.get_serializer(user)
        return Response(serializer.data)


class UpdateUser(generics.UpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = AccountSerializer


class GetUser(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = AccountSerializer
    pagination_class = UserPagination


class CreateUser(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer


class GetUserById(generics.RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = AccountSerializer

    def retrieve(self, request, *args, **kwargs):
        user_id = kwargs.get("pk")
        user = get_object_or_404(self.get_queryset(), pk=user_id)
        serializer = self.get_serializer(user)
        return Response(serializer.data)


class DeleteUserById(generics.DestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = AccountSerializer

    def delete(self, request, *args, **kwargs):
        user_id = kwargs.get('pk')
        user_instance = get_object_or_404(CustomUser, id=user_id)
        user_instance.state = 0
        user_instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
