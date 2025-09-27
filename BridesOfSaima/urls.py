from django.urls import path
from . import views

app_name = 'BridesOfSaima'

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('my-brides/', views.brides_gallery, name='brides_gallery'),
    path('my-brides/<int:pk>/', views.bride_detail, name='bride_detail'),
    
    # Invoice URLs
    path('invoices/', views.invoice_list, name='invoice_list'),
    path('invoices/create/', views.invoice_create, name='invoice_create'),
    path('invoices/<int:pk>/', views.invoice_detail, name='invoice_detail'),
    path('invoices/<int:pk>/edit/', views.invoice_edit, name='invoice_edit'),
    path('invoices/<int:pk>/print/', views.invoice_print, name='invoice_print'),
    
    # Customer URLs
    path('customers/create/', views.customer_create, name='customer_create'),
]