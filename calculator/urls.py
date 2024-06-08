from django.urls import path
from .views import ViewNum

urlpatterns = [
    path('numbers/<str:numberid>/', ViewNum.as_view(), name='numbers'),
]