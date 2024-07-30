from django.urls import path
from .views import SuccessView, UserCreate

urlpatterns = [
    path('signup/', UserCreate.as_view(), name='signup'),
    path('success/', SuccessView.as_view(), name='success'),   
]
