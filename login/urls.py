from django.urls import path
from .views import signup,profile, login,logout, home, dashboard, forgot_password, reset_password,reset_password_confirm

urlpatterns = [
    path('', home, name='home'),
    path('signup/', signup, name='signup'),
    path('login/', login, name='login'),
    path('dashboard/',dashboard,name='dashboard'),
    path('forgot_password/',forgot_password,name='forgot_password'),
    path('reset_password/<str:token>/', reset_password, name='reset_password'),
    path('reset_password_confirm/',reset_password_confirm,name='reset_password_confirm'),
    path('logout/',logout, name='logout'),
    path('profile/',profile,name='profile'),
    # Add other URLs as needed
]
