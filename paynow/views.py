
# ============================================================================
# paynow/views.py
# ============================================================================
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from rest_framework.viewsets import ModelViewSet

from .models import PayNowPayment, PayNowStatusUpdate
from .serializers import (
    PayNowPaymentListSerializer,
    PayNowPaymentDetailSerializer,
    PayNowPaymentCreateSerializer,
)
from .paynow_client import PayNowClient
from .utils import verify_hash, parse_paynow_response
from . import conf


def get_client_ip(request):
    """Get client IP address"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


@login_required
def checkout_view(request):
    """Create payment and redirect to PayNow"""
    
    # Get payment details from query params
    amount = request.GET.get('amount', '10.00')
    description = request.GET.get('description', 'Payment')
    email = request.GET.get('email', request.user.email)
    phone = request.GET.get('phone', '')
    
    # Create payment record
    payment = PayNowPayment.objects.create(
        user=request.user,
        amount=amount,
        description=description,
        email=email,
        phone=phone,
    )
    
    # Build callback URLs
    return_url = request.build_absolute_uri(
        reverse('paynow:payment_return', kwargs={'reference': payment.reference})
    )
    result_url = request.build_absolute_uri(reverse('paynow:payment_result'))
    
    # Initialize transaction with PayNow
    client = PayNowClient()
    result = client.initiate_transaction({
        'reference': payment.reference,
        'amount': payment.amount,
        'description': payment.description,
        'email': payment.email,
        'phone': payment.phone,
        'returnurl': return_url,
        'resulturl': result_url,
    })
    
    if result['success']:
        # Update payment with PayNow data
        payment.poll_url = result['poll_url']
        payment.browser_url = result['browser_url']
        payment.hash_value = result['hash']
        payment.status = 'sent'
        payment.save()
        
        # Redirect to PayNow
        return redirect(result['browser_url'])
    else:
        # Handle error
        payment.status = 'failed'
        payment.additional_info = result.get('error', 'Unknown error')
        payment.save()
        
        return render(request, 'paynow/payment_error.html', {
            'payment': payment,
            'error': result.get('error', 'Failed to initialize payment'),
        })


def payment_detail_view(request, reference):
    """View payment details"""
    payment = get_object_or_404(PayNowPayment, reference=reference)
    
    return render(request, 'paynow/payment_detail.html', {
        'payment': payment,
    })


def payment_return_view(request, reference):
    """Handle return from PayNow"""
    payment = get_object_or_404(PayNowPayment, reference=reference)
    
    # Check payment status
    if payment.poll_url:
        client = PayNowClient()
        status = client.check_transaction_status(payment.poll_url)
        
        if status['success']:
            # Update payment status
            payment_status = status['status'].lower()
            
            if payment_status == 'paid':
                payment.mark_paid()
                payment.paynow_reference = status.get('paynow_reference', '')
                payment.save()
                
                return render(request, 'paynow/payment_success.html', {
                    'payment': payment,
                })
    
    return render(request, 'paynow/payment_pending.html', {
        'payment': payment,
    })


@csrf_exempt
@require_POST
def payment_result_view(request):
    """Handle PayNow result callback (webhook)"""
    
    # Parse POST data
    data = request.POST.dict()
    
    # Get payment reference
    reference = data.get('reference')
    if not reference:
        return HttpResponse('Invalid request', status=400)
    
    try:
        payment = PayNowPayment.objects.get(reference=reference)
    except PayNowPayment.DoesNotExist:
        return HttpResponse('Payment not found', status=404)
    
    # Verify hash
    received_hash = data.get('hash', '')
    hash_data = {k: v for k, v in data.items() if k != 'hash'}
    hash_valid = verify_hash(hash_data, received_hash, conf.PAYNOW_INTEGRATION_KEY)
    
    # Log status update
    status_update = PayNowStatusUpdate.objects.create(
        payment=payment,
        status=data.get('status', ''),
        paynow_reference=data.get('paynowreference', ''),
        amount=data.get('amount'),
        raw_response=data,
        hash_verified=hash_valid,
        ip_address=get_client_ip(request),
    )
    
    if hash_valid:
        # Update payment status
        status = data.get('status', '').lower()
        payment.paynow_reference = data.get('paynowreference', '')
        
        if status == 'paid':
            payment.mark_paid()
        elif status == 'cancelled':
            payment.mark_cancelled()
        else:
            payment.status = status
        
        payment.save()
    
    return HttpResponse('OK', status=200)


class PayNowPaymentViewSet(ModelViewSet):
    """API ViewSet for PayNow payments"""
    
    queryset = PayNowPayment.objects.all()
    lookup_field = 'reference'
    
    serializer_classes = {
        'list': PayNowPaymentListSerializer,
        'retrieve': PayNowPaymentDetailSerializer,
        'create': PayNowPaymentCreateSerializer,
    }
    
    def get_serializer_class(self):
        return self.serializer_classes.get(
            self.action,
            PayNowPaymentCreateSerializer
        )


