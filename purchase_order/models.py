from django.db import models
from vendors.models import Vendor

# Create your models here.
class PurchaseOrder(models.Model):
    po_number = models.CharField(max_length=100,unique=True,blank=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE,null=True, db_constraint=False)
    order_date = models.DateTimeField()
    delivery_date = models.DateTimeField()
    items = models.JSONField()
    quantity = models.IntegerField(blank=True)
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    status = models.CharField(max_length=255, choices=STATUS_CHOICES, default='pending')
    quality_rating = models.FloatField(null=True,blank=True)
    issue_date = models.DateTimeField(null=True,blank=True)
    acknowledgment_date = models.DateTimeField(null=True,blank=True)
    completion_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.po_number