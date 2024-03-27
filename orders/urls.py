from django.urls import path
from . import views

urlpatterns = [
    path('order-history/<str:username>/', views.get_order_history),
    path('place-order/', views.PlaceOrderAPIView.as_view(), name='place_order'),

    #address api endpoint
    path('get-address/<str:username>/', views.get_addresses_by_username),
    path('add-address/', views.add_address),
    path('edit-address/<int:pk>/', views.edit_address),
    path('delete-address/<int:pk>/', views.delete_address),

    #wishlist api endpoint
    path('get-wishlist/<str:username>/', views.get_wishlist),
    path('add-wishlist-item/', views.add_wishlist_item),
    path('delete-wishlist-item/<int:pk>/', views.delete_wishlist_item),

]