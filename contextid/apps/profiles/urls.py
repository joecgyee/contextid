from django.urls import path
from . import views

app_name = "profiles"

urlpatterns = [
    path('<int:pk>/', views.IdentityProfileDetail.as_view(), name='profile_detail'),
    path('create/', views.IdentityProfileCreate.as_view(), name='profile_create'),
    path('update/<int:pk>/', views.IdentityProfileUpdate.as_view(), name='profile_update'),
    path('delete/<int:pk>/', views.IdentityProfileDelete.as_view(), name='profile_delete'),
]
