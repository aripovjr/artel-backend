from django.urls import path
from .views import *


urlpatterns = [
    path("check_id/", AccountCheckerByID.as_view()),
    path("check_number/", AccountCheckerByPhoneNumber.as_view()),
    path("update_user/<int:pk>/", UpdateUser.as_view()),
    path("get_user/", GetUser.as_view()),
    path("create_user", CreateUser.as_view()),
    path("get_user_by_id/<int:pk>", GetUserById.as_view())
]
