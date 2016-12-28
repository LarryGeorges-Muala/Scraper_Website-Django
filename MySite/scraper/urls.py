from django.conf.urls import url 
from . import views

app_name = 'scraper'

urlpatterns=[

	url(r'^$', views.home, name='home'),
	url(r'^gumtree/$', views.scrapGumtree, name='scrapGumtree'),
	url(r'^about/$', views.about, name='about'),
	url(r'^cars/$', views.scrapCars, name='scrapCars'),
	
]