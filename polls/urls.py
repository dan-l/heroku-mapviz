from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^score/([0-9]{4})$', views.score),
    url(r'^sentiment/?$', views.sentiment),
    url(r'^tweets/?$', views.tweets)
]