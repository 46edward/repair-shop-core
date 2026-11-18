class RepairShopError(Exception):
    """Base exception for all errors"""
    pass

class InvalidCostError(RepairShopError, ValueError):
    pass

class OutOfStockError(RepairShopError):
    """Ощибка при попытке списать больше запчастей чем есть на складе"""
    pass
