from django.db import models
from datetime import datetime

class HistoricalStockCache(models.Model):
    """
    A simple class to cache historical stock levels by month/year per product/facility
    """        
    supply_point = models.ForeignKey('logistics.SupplyPoint')
    product = models.ForeignKey('logistics.Product', null=True)
    year = models.PositiveIntegerField()
    month = models.PositiveIntegerField()
    stock = models.IntegerField(null=True)
    

class ReportingModel(models.Model):
    """
    A model to encapsulate aggregate (data warehouse) data used by a report.
    """
    supply_point = models.ForeignKey('logistics.SupplyPoint') # viewing supply point
    date = models.DateTimeField()                   # viewing time period
    create_date = models.DateTimeField(editable=False)
    update_date = models.DateTimeField(editable=False)

    def save(self, *args, **kwargs):
        if not self.id:
            self.create_date = datetime.utcnow()
        self.update_date = datetime.utcnow()
        super(ReportingModel, self).save(*args, **kwargs)

    class Meta:
        abstract = True

    