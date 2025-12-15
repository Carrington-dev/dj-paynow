
# ============================================================================
# paynow/urls.py
# ============================================================================
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'paynow'

router = DefaultRouter()
router.register('payments', views.PayNowPaymentViewSet, basename='payment')

urlpatterns = [
    # Web views
    path('checkout/', views.checkout_view, name='checkout'),
    path('payment/<str:reference>/', views.payment_detail_view, name='payment_detail'),
    path('return/<str:reference>/', views.payment_return_view, name='payment_return'),
    
    # Webhook
    path('result/', views.payment_result_view, name='payment_result'),
    
    # API
    path('', include(router.urls)),
]
