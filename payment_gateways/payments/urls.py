from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('create-checkout-session/', views.create_checkout_session, name='checkout'),
    path('webhook/', views.stripe_webhook, name='stripe-webhook'),
    path('success/', views.success, name='success'),
    path('cancel/', views.cancel, name='cancel'),
]