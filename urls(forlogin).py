from django.urls import path 
from .views import login_view, users_view, logout_view, user_stats_view 

urlpatterns = [
    path('', login_view, name='login'), 
    path('users/', users_view, name='users'), 
    path('logout/', logout_view, name='logout'),  # Fixed here
    path('user_stats/', user_stats_view, name='user_stats'), 
]
