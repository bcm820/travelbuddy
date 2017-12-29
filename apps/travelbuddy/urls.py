from django.conf.urls import url
from . import views

urlpatterns = [
    
    # Login & Registration #
    url(r'^$', views.index),
    url(r'^register/$', views.register),
    url(r'^login/$', views.login),
    url(r'^logout/$', views.logout),

    # Main Site Pages
    url(r'^travels/$', views.main),
    url(r'^travels/add/$', views.add),
    url(r'^travels/trip/(?P<id>\d+)/$', views.show),
    url(r'^travels/users/$', views.UsersView.as_view()),

    # User Actions #
    url(r'^travels/add/post/$', views.post),
    url(r'^travels/trip/(?P<id>\d+)/join/$', views.join),

]