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
    path("signup/", views.signup, name="signup"),
    path("search/q1/", views.query1, name="query1"),
    path("search/q2/", views.query2, name="query2"),
    path("search/q3/", views.query3, name="query3"),
]