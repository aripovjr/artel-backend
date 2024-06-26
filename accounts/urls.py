from django.urls import path
from .views import *


urlpatterns = [
    path("check_id/", AccountCheckerByID.as_view()),
    path("check_number/", AccountCheckerByPhoneNumber.as_view()),
    path("update_user/<int:pk>/", UpdateUser.as_view()),
]
