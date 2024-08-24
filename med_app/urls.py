from django.urls import path,include
from . import views

urlpatterns = [

    path('base', views.base, name='base'),
    path('', views.index, name='index'),
    path('signup', views.signup, name='signup'),
    path('contact_us', views.contact_us, name='contact_us'),
    path('checkout/', views.checkout, name='checkout'),
    path('order/', views.your_order, name='order'),
    path('product/', views.product_page, name='product'),
    path('product/<str:id>', views.product_detail, name='product_detail'),
    path('search/', views.search_product, name='search'),

]
