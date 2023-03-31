from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('car/<str:product>', views.product),
    path('shopping-car/', views.shoppingCar),
    path('add-shopping-car/', views.addProductToCar),
    path('search/', views.searchProducts),
]
