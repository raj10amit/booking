from django.urls import path
from . import views

urlpatterns = [
    path('book/', views.book_item, name='book_item'),
    path('cancel/', views.cancel_booking, name='cancel_booking'),
]
