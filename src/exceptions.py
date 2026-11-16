class RepairShopError(Exception):
    """Base exception for all errors"""
    pass

class InvalidCostError(RepairShopError, ValueError):
    pass