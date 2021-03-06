from dimagi.utils.modules import to_function
from logistics.exceptions import TooMuchStockError
from logistics.models import ProductStock
from rapidsms.conf import settings


def check_max_levels(stock_report):
    """
    checks a stock report against maximum allowable levels. if more than the
    allowable threshold of stock is being reported it throws a validation error
    """
    for product_code, stock in stock_report.product_stock.items():
        product = stock_report.get_product(product_code)
        try:
            current_stock = ProductStock.objects.get(supply_point=stock_report.supply_point,
                                                     product=product)
            max = current_stock.maximum_level * settings.LOGISTICS_MAX_REPORT_LEVEL_FACTOR
            if stock > max:
                raise TooMuchStockError(product=product, amount=stock, max=max)
        except ProductStock.DoesNotExist:
            pass

def get_max_level_function():
    if settings.LOGISTICS_MAX_REPORT_LEVEL_FUNCTION:
        return to_function(settings.LOGISTICS_MAX_REPORT_LEVEL_FUNCTION)
    elif settings.LOGISTICS_MAX_REPORT_LEVEL_FACTOR:
        return check_max_levels
    else:
        return None
