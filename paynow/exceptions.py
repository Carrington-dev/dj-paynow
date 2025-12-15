
# ============================================================================
# paynow/exceptions.py
# ============================================================================

class PayNowError(Exception):
    """Base exception for PayNow errors"""
    pass


class PayNowConfigurationError(PayNowError):
    """Configuration error"""
    pass


class PayNowAPIError(PayNowError):
    """API communication error"""
    pass


class PayNowValidationError(PayNowError):
    """Validation error"""
    pass


# ============================================================================
# End of dj-paynow package
# ============================================================================