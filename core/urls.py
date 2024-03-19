from django.urls import path
from . import views

from core.views import contact

app_name = 'core'

urlpatterns = [
    path('', views.index, name='index'),
    path('contact/', contact, name='contact'),
    path('signup/', views.signup, name='signup')
]