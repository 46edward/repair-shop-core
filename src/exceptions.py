class RepairShopError(Exception):
    """Base exception for all errors"""
    pass

class InvalidCostError(RepairShopError, ValueError):
    pass

class OutOfStockError(RepairShopError):
    """Ощибка при попытке списать больше запчастей чем есть на складе"""
    pass

class EntityNotFoundError(RepairShopError):
    """Base error"""

class OrderNotFoundError(EntityNotFoundError):
    """Order not found by ID"""
    pass

class ClientNotFoundError(EntityNotFoundError):
    """Client fot found"""
    pass

class PartNotFoundError(EntityNotFoundError):
    """Part not found by ID"""
    pass