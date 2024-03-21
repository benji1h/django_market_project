from django.urls import path
from . import views

app_name = 'item'

urlpatterns = [
    path('itemsstripes', views.itemsstripes, name='itemsstripes'),
    path('', views.items, name='items'),
    path('new/', views.new, name='new'),
    path('<int:pk>/', views.detail, name="detail"),
    path('<int:pk>/delete/', views.delete, name="delete"),
    path('<int:pk>/edit/', views.edit, name="edit"),
    path('config/', views.stripe_config, name="stripe_config"),
    path('create-checkout-session/', views.create_checkout_session, name="create_checkout_session"),
    path('success/', views.SuccessView.as_view()), 
    path('cancelled/', views.CancelledView.as_view()),
]