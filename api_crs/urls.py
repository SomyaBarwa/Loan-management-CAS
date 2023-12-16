from django.urls import path, include

from rest_framework import routers

from . import views

routers = routers.DefaultRouter()

urlpatterns = [
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('register/', views.CustomerCreateAPIView.as_view()),
    path('customers/', views.CustomerListAPIView.as_view()),
    path('create-loan/', views.LoanCreateAPIView.as_view(), name='loan-create'),
    path('loan/', views.LoanListAPIView.as_view(), name='loan-list'),
    path('view-loan/<int:pk>/', views.LoanDetailAPIView.as_view(), name='loan-detail'),
    path('view-loan/customer/<int:pk>/', views.CustomerLoanListAPIView.as_view(), name='loan-list-by-customer')
]

urlpatterns += routers.urls
