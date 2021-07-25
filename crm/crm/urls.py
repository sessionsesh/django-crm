"""crm URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from accounts.views import home, register, login_, logout_
from orders.views import orders, delete_order, create_customer_create_order, leave_order

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', home),
    path('register/', register),
    path('orders/', orders),
    path('login', login_),
    path('logout', logout_),
    path('delete/orders/<ID>', delete_order),
    path('leave/orders/<ID>', leave_order),
    path('create_by_phone_number', create_customer_create_order),
]
