from django.urls import path
from . import views

urlpatterns = [
    path("", views.signup, name="signup"),
    # path('resend-verification/', views.resend_verification, name='resend_verification'),
    path("verify/", views.verify_email, name="verify_email"),
    
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('home/', views.home, name='home'),
]
