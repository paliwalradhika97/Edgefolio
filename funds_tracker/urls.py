from django.urls import path
from .views import *

urlpatterns = [
    path('api/fund/', FundAPI.as_view(), name='fund'),
    path('api/fund-detail/<int:pk>', FundObjectAPI.as_view(), name='fund-detail'),
    path('', home, name='home')
]