from django.urls import path
from django.views.generic import TemplateView
from . import views

app_name = "main"

urlpatterns = [
    path("", views.index, name="index"),
    path("home/", views.home, name="home"),
    path("about-us/", views.aboutUs, name="aboutUs"),
    path("contact-us/", views.contactUs, name="contactUs"),
    path("login/", views.loginview, name="login"),
    path("logout/", views.logoutview, name="logout"),
    path("search/", views.searchresult, name="searchresult"),
    path("mail/", views.mail, name="mail"),
    path("success/", views.success, name="success"),
    path("email/", views.emailview, name="email"),
    path("signup/", views.signup, name="signup"),
    path("headerleft/", views.headerleft, name="headerleft"),
    path("headerright/", views.headerright, name="headerright"),
    path("default/", views.default, name="default"),
]