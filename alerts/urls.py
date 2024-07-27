from django.urls import path
from .views import AlertCreateView, AlertDeleteView, AlertListView

urlpatterns = [
    path('create/', AlertCreateView.as_view(), name='alert-create'),
    path('delete/<int:pk>/', AlertDeleteView.as_view(), name='alert-delete'),
    path('', AlertListView.as_view(), name='alert-list'),
]
