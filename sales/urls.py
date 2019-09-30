from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('log', views.login, name='login'),
    path('logout', views.logout, name='logout'),

    path('', views.index, name='index'),
    path('login', views.login_view, name='login'),
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('adminpage', views.admin_dash, name='admin_dash'),
    path('customerpage', views.customer_dash, name='customer_dash'),
    path('shoppage', views.shop_dash, name='shop_dash'),
    path('shopsignup', views.shop_sign, name='shop_sign'),

    #Shop
    path('shop', views.shop, name= 'shop'),
    path('shopshow', views.shopshow),
    path('shopedit/<int:id>', views.shopedit),
    path('shopupdate/<int:id>', views.shopupdate),
    path('shopdestroy/<int:id>',views.shopdestroy),

    #Customer
    path('customer', views.customer, name='customer'),
    path('customershow', views.customershow),
    path('customeredit/<int:id>', views.customeredit),
    path('customerupdate/<int:id>', views.customerupdate),
    path('customerdestroy/<int:id>', views.customerdestroy),

    path('product', views.product, name='product'),
    path('productshow', views.productshow, name = 'productshow'),
    path('productedit/<int:id>', views.productedit),
    path('productupdate/<int:id>', views.productupdate),
    path('productdestroy/<int:id>', views.productdestroy),

    path('deal', views.deal, name = 'deal'),
    path('dealshow', views.dealshow, name ='dealshow'),
    path('dealedit/<int:id>', views.dealedit),
    path('dealupdate/<int:id>', views.dealupdate),
    path('dealdestroy/<int:id>', views.dealdestroy),
    path('dealapprove/<int:id>', views.approve_deal, name='dealapprove'),
    path('productapprove/<int:id>', views.approve_product, name='productapprove'),
    path('find', views.find, name='find'),
    path('shopinfo/<int:id>', views.shop_info, name= 'shop_info')
]