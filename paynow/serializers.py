# ============================================================================
# paynow/serializers.py
# ============================================================================
from rest_framework import serializers
from .models import PayNowPayment, PayNowStatusUpdate


class PayNowPaymentListSerializer(serializers.ModelSerializer):
    """Serializer for listing PayNow payments"""
    
    user_email = serializers.EmailField(source='user.email', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = PayNowPayment
        fields = [
            'id',
            'reference',
            'user',
            'user_email',
            'amount',
            'description',
            'status',
            'status_display',
            'created_at',
            'paid_at',
        ]
        read_only_fields = ['reference', 'created_at', 'paid_at']


class PayNowPaymentDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for PayNow payment"""
    
    paynow_url = serializers.SerializerMethodField()
    
    class Meta:
        model = PayNowPayment
        fields = [
            'id',
            'reference',
            'amount',
            'description',
            'email',
            'phone',
            'paynow_url',
            'status',
            'payment_method',
            'created_at',
        ]
        read_only_fields = ['reference', 'created_at']
    
    def get_paynow_url(self, obj):
        """Get the absolute URL for this payment"""
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(obj.get_absolute_url())
        return obj.get_absolute_url()


class PayNowPaymentCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating PayNow payments"""
    
    paynow_url = serializers.SerializerMethodField()
    
    class Meta:
        model = PayNowPayment
        fields = [
            'id',
            'user',
            'amount',
            'description',
            'email',
            'phone',
            'paynow_url',
            'custom_str1',
            'custom_str2',
            'custom_str3',
            'custom_int1',
            'custom_int2',
        ]
    
    def validate_amount(self, value):
        """Validate amount is positive"""
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than zero")
        return value
    
    def get_paynow_url(self, obj):
        """Get the absolute URL for this payment"""
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(obj.get_absolute_url())
        return obj.get_absolute_url()


class PayNowStatusUpdateSerializer(serializers.ModelSerializer):
    """Serializer for status updates"""
    
    payment_reference = serializers.CharField(source='payment.reference', read_only=True)
    
    class Meta:
        model = PayNowStatusUpdate
        fields = [
            'id',
            'payment',
            'payment_reference',
            'status',
            'paynow_reference',
            'amount',
            'hash_verified',
            'created_at',
        ]
        read_only_fields = '__all__'


