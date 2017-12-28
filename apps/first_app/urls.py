from django.conf.urls import url
from . import views           # This line is new!



urlpatterns = [
    url(r'^$', views.index),
    url(r'^create$', views.create),
    url(r'^get_infomoney$', views.get_infomoney),
    url(r'^get_valor$', views.get_valor),
    url(r'^get_g1$', views.get_g1),     # This line has changed!
    url(r'^get_estadao$', views.get_estadao),
    url(r'^get_folha$', views.get_folha),
    url(r'^get_all$', views.get_all),
    url(r'^get_search$', views.get_search), 
  ]

