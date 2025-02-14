from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name="home"),
    path('register', views.register, name="register"),
    path('login', views.login_user, name="login"),
    path('logout', views.logout_user, name="logout"),
    path('pinjam', views.pinjam, name="pinjam"),
    path('history', views.history, name="history"),
    path('balikin', views.balikin, name="balikin")
]