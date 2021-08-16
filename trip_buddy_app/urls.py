from django.urls import path
from .views import *

urlpatterns = [
    path('', login_reg),
    path('user/register', create_user),
    path('dashboard', trips),
    path('add_trip', add_trip),
    path('create_trip', create_trip),
    path('<int:trip_id>/trip_details', trip_details),
    path('<int:trip_id>/edit_trips', edit_trips),
    path('<int:trip_id>/update', update),
    path('user/login', login_user),
    path('user/logout', logout),
    path('<int:trip_id>/delete', delete),
    
]