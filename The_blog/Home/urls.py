from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.blank, name='blank'),
    path('contact', views.contact, name='contact'),
    path('about', views.about, name='about'),
    path('search', views.search, name='search'),
    path('signup', views.handlesignup, name='handlesignup'),
    path('login', views.handleslogin, name='handleslogin'),
    path('Logout', views.handleslogout, name='handleslogout')
]