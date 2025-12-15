import requests
from . import conf
from .utils import generate_hash, parse_paynow_response


class PayNowClient:
    """Client for interacting with PayNow API"""
    
    def __init__(self):
        self.integration_id = conf.PAYNOW_INTEGRATION_ID
        self.integration_key = conf.PAYNOW_INTEGRATION_KEY
        self.init_url = conf.PAYNOW_INIT_URL
        self.status_url = conf.PAYNOW_STATUS_URL
    
    def initiate_transaction(self, payment_data):
        """
        Initiate transaction with PayNow
        
        Args:
            payment_data: Dictionary containing:
                - reference: Unique payment reference
                - amount: Payment amount
                - description: Payment description
                - email: Customer email
                - returnurl: Return URL
                - resulturl: Result URL (webhook)
                - authemail: (optional) Auth email
                - phone: (optional) Phone number
        
        Returns:
            Dictionary with response data
        """
        # Build request data
        data = {
            'id': self.integration_id,
            'reference': payment_data['reference'],
            'amount': str(payment_data['amount']),
            'additionalinfo': payment_data.get('description', ''),
            'returnurl': payment_data['returnurl'],
            'resulturl': payment_data['resulturl'],
            'authemail': payment_data.get('email', ''),
            'status': 'Message',
        }
        
        # Add optional phone
        if payment_data.get('phone'):
            data['phone'] = payment_data['phone']
        
        # Generate hash (exclude status from hash)
        hash_data = {k: v for k, v in data.items() if k != 'status'}
        data['hash'] = generate_hash(hash_data, self.integration_key)
        
        # Make request
        try:
            response = requests.post(
                self.init_url,
                data=data,
                timeout=30
            )
            response.raise_for_status()
            
            # Parse response
            result = parse_paynow_response(response.text)
            
            return {
                'success': result.get('status', '').lower() == 'ok',
                'status': result.get('status', ''),
                'poll_url': result.get('pollurl', ''),
                'browser_url': result.get('browserurl', ''),
                'hash': result.get('hash', ''),
                'error': result.get('error', ''),
                'raw_response': result,
            }
            
        except requests.RequestException as e:
            return {
                'success': False,
                'error': str(e),
                'raw_response': {},
            }
    
    def check_transaction_status(self, poll_url):
        """
        Check transaction status using poll URL
        
        Args:
            poll_url: Poll URL from initiate_transaction response
        
        Returns:
            Dictionary with status data
        """
        try:
            response = requests.post(poll_url, timeout=30)
            response.raise_for_status()
            
            # Parse response
            result = parse_paynow_response(response.text)
            
            return {
                'success': True,
                'status': result.get('status', ''),
                'reference': result.get('reference', ''),
                'paynow_reference': result.get('paynowreference', ''),
                'amount': result.get('amount', ''),
                'hash': result.get('hash', ''),
                'raw_response': result,
            }
            
        except requests.RequestException as e:
            return {
                'success': False,
                'error': str(e),
                'raw_response': {},
            }


