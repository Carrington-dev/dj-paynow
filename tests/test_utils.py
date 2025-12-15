from django.test import TestCase
from paynow.utils import (
    generate_payment_id,
    generate_hash,
    verify_hash,
    parse_paynow_response,
)


class UtilsTest(TestCase):
    """Test utility functions"""
    
    def test_generate_payment_id_default(self):
        """Test generating payment ID with defaults"""
        payment_id = generate_payment_id()
        
        self.assertTrue(payment_id.startswith('PN'))
        self.assertEqual(len(payment_id), 12)
        self.assertTrue(payment_id[2:].isalnum())
    
    def test_generate_payment_id_custom_prefix(self):
        """Test generating payment ID with custom prefix"""
        payment_id = generate_payment_id(prefix='TEST')
        
        self.assertTrue(payment_id.startswith('TEST'))
        self.assertEqual(len(payment_id), 12)
    
    def test_generate_payment_id_custom_length(self):
        """Test generating payment ID with custom length"""
        payment_id = generate_payment_id(length=20)
        
        self.assertEqual(len(payment_id), 20)
        self.assertTrue(payment_id.startswith('PN'))
    
    def test_generate_payment_id_uniqueness(self):
        """Test that generated IDs are unique"""
        ids = set()
        for _ in range(100):
            ids.add(generate_payment_id())
        
        # All 100 should be unique
        self.assertEqual(len(ids), 100)
    
    def test_generate_hash(self):
        """Test hash generation"""
        data = {
            'id': '12345',
            'reference': 'REF123',
            'amount': '100.00',
        }
        integration_key = 'test_key'
        
        hash_value = generate_hash(data, integration_key)
        
        self.assertIsInstance(hash_value, str)
        self.assertEqual(len(hash_value), 128)  # SHA512 produces 128 hex chars
        self.assertTrue(hash_value.isupper())
    
    def test_generate_hash_consistency(self):
        """Test that same data produces same hash"""
        data = {'key': 'value', 'amount': '100'}
        integration_key = 'test_key'
        
        hash1 = generate_hash(data, integration_key)
        hash2 = generate_hash(data, integration_key)
        
        self.assertEqual(hash1, hash2)
    
    def test_generate_hash_sorting(self):
        """Test that hash is order-independent (sorted by keys)"""
        data1 = {'b': '2', 'a': '1', 'c': '3'}
        data2 = {'a': '1', 'c': '3', 'b': '2'}
        integration_key = 'test_key'
        
        hash1 = generate_hash(data1, integration_key)
        hash2 = generate_hash(data2, integration_key)
        
        self.assertEqual(hash1, hash2)
    
    def test_verify_hash_valid(self):
        """Test verifying valid hash"""
        data = {'key': 'value', 'amount': '100'}
        integration_key = 'test_key'
        
        generated_hash = generate_hash(data, integration_key)
        is_valid = verify_hash(data, generated_hash, integration_key)
        
        self.assertTrue(is_valid)
    
    def test_verify_hash_invalid(self):
        """Test verifying invalid hash"""
        data = {'key': 'value', 'amount': '100'}
        integration_key = 'test_key'
        wrong_hash = 'INVALID_HASH'
        
        is_valid = verify_hash(data, wrong_hash, integration_key)
        
        self.assertFalse(is_valid)
    
    def test_verify_hash_case_insensitive(self):
        """Test that hash verification is case insensitive"""
        data = {'key': 'value'}
        integration_key = 'test_key'
        
        hash_upper = generate_hash(data, integration_key)
        hash_lower = hash_upper.lower()
        
        self.assertTrue(verify_hash(data, hash_lower, integration_key))
        self.assertTrue(verify_hash(data, hash_upper, integration_key))
    
    def test_parse_paynow_response_simple(self):
        """Test parsing simple PayNow response"""
        response = "status=ok\nreference=REF123\namount=100.00"
        
        result = parse_paynow_response(response)
        
        self.assertEqual(result['status'], 'ok')
        self.assertEqual(result['reference'], 'REF123')
        self.assertEqual(result['amount'], '100.00')
    
    def test_parse_paynow_response_with_equals(self):
        """Test parsing response with = in values"""
        response = "key=value=with=equals\nother=normal"
        
        result = parse_paynow_response(response)
        
        self.assertEqual(result['key'], 'value=with=equals')
        self.assertEqual(result['other'], 'normal')
    
    def test_parse_paynow_response_empty(self):
        """Test parsing empty response"""
        response = ""
        
        result = parse_paynow_response(response)
        
        self.assertEqual(result, {})
    
    def test_parse_paynow_response_whitespace(self):
        """Test parsing response with whitespace"""
        response = "  status = ok  \n  reference = REF123  "
        
        result = parse_paynow_response(response)
        
        self.assertEqual(result['status'], 'ok')
        self.assertEqual(result['reference'], 'REF123')
    
    def test_parse_paynow_response_real_example(self):
        """Test parsing real PayNow response format"""
        response = """status=Ok
browserurl=https://www.paynow.co.zw/payment/pay.aspx?guid=abc123
pollurl=https://www.paynow.co.zw/interface/pollurl?guid=abc123
hash=ABCDEF123456"""
        
        result = parse_paynow_response(response)
        
        self.assertEqual(result['status'], 'Ok')
        self.assertTrue('paynow.co.zw' in result['browserurl'])
        self.assertTrue('paynow.co.zw' in result['pollurl'])
        self.assertEqual(result['hash'], 'ABCDEF123456')
    
    def test_parse_paynow_response_no_equals(self):
        """Test parsing lines without equals sign"""
        response = "invalid line\nstatus=ok\nanother invalid"
        
        result = parse_paynow_response(response)
        
        # Should only parse valid lines
        self.assertEqual(result, {'status': 'ok'})