from django.urls import path
from .views import extract_text_via_flask

urlpatterns = [
    path('extract/', extract_text_via_flask, name='extract_text_via_flask'),
]
