from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('stores/', views.stores_list, name='stores'),
    path('store/<int:store_id>/', views.store_detail, name='store_detail'),
    path('seller/', views.seller_panel, name='seller_panel'),
    path('customer/', views.customer_panel, name='customer_panel'),

    path('cart/', views.cart_view, name='cart'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('payment/', views.payment, name='payment'),

    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html') ,name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='registration/logged_out.html') ,name='logout'),
]
