from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('car/<str:product_ID>', views.product),
    path('category/<str:name>', views.category),
    path('shopping-car/', views.shoppingCar),
    path('add-shopping-car/', views.addProductToCar),
    path('search/', views.searchProducts),
    path('checkout/', views.checkout),
    path('code/', views.redeemPromoCode),
    path('payment/', views.payment),
    path('thanks/<str:order>', views.thanks),
]
