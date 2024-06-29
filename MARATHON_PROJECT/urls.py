
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('base_app.urls')),
    path('admin/', admin.site.urls),
]
#apa tuna fanya ku include urls.py ambayo ipo kwenye app yangu