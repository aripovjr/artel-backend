from django.shortcuts import render, get_object_or_404
from rest_framework import generics
from rest_framework.response import Response
from .models import CustomUser
from .serializers import AccountSerializer


class AccountCheckerByID(generics.GenericAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = AccountSerializer

    def get(self, request, *args, **kwargs):
        user_id = request.POST.get("telegram_id")
        user = get_object_or_404(CustomUser, telegram_id=user_id)
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


