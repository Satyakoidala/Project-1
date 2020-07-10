from django.urls import path
from . import views

app_name = "main"

urlpatterns = [
    path('',views.index, name = "index"),
    path('home/',views.home, name = "home"),
    path('about-us/',views.aboutUs, name = "aboutUs"),
    path('contact-us/',views.contactUs, name = "contactUs"),
    path('login/',views.loginview, name = "login"),
    path('logout/',views.logoutview, name = "logout"),
    path('search/',views.searchresult, name = "searchresult"),
]