from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import PurchaseOrder, Vendor
from django.utils import timezone
from vendors.models import HistoricalPerformance

@receiver(post_save, sender=PurchaseOrder)
def update_on_time_delivery_rate(sender, instance, **kwargs):
    if instance.status == 'completed' and not instance.completion_date:
        instance.completion_date = timezone.now()
        instance.save(update_fields=['completion_date'])
        
        vendor = instance.vendor
        completed_pos = PurchaseOrder.objects.filter(vendor=vendor, status='completed')
        on_time_pos = completed_pos.filter(delivery_date__gte=instance.delivery_date)
        
        if completed_pos.exists():
            on_time_delivery_rate = on_time_pos.count() / completed_pos.count()
            vendor.on_time_delivery_rate = on_time_delivery_rate * 100  # as a percentage
            vendor.save()
            
            # Save historical performance
            save_historical_performance(vendor)

@receiver(post_save, sender=PurchaseOrder)
def update_quality_rating_avg(sender, instance, **kwargs):
    if instance.status == 'completed' and instance.quality_rating is not None:
        vendor = instance.vendor
        completed_pos = PurchaseOrder.objects.filter(vendor=vendor, status='completed', quality_rating__isnull=False)
        
        if completed_pos.exists():
            total_quality_rating = sum(po.quality_rating for po in completed_pos)
            quality_rating_avg = total_quality_rating / completed_pos.count()
            vendor.quality_rating_avg = quality_rating_avg
            vendor.save()
            
            # Save historical performance
            save_historical_performance(vendor)

@receiver(post_save, sender=PurchaseOrder)
def update_average_response_time(sender, instance, **kwargs):
    if instance.acknowledgment_date:
        vendor = instance.vendor
        purchase_orders = PurchaseOrder.objects.filter(vendor=vendor, acknowledgment_date__isnull=False)
        
        if purchase_orders.exists():
            total_response_time = 0
            for po in purchase_orders:
                total_response_time += (po.acknowledgment_date - po.issue_date).total_seconds()
            
            average_response_time = total_response_time / purchase_orders.count()
            vendor.average_response_time = average_response_time
            vendor.save()
            
            # Save historical performance
            save_historical_performance(vendor)

@receiver(post_save, sender=PurchaseOrder)
def update_fulfillment_rate(sender, instance, **kwargs):
    vendor = instance.vendor
    all_pos = PurchaseOrder.objects.filter(vendor=vendor)
    completed_pos = all_pos.filter(status='completed')
    
    if all_pos.exists():
        fulfillment_rate = completed_pos.count() / all_pos.count()
        vendor.fulfillment_rate = fulfillment_rate * 100  # as a percentage
        vendor.save()
        
        # Save historical performance
        save_historical_performance(vendor)

def save_historical_performance(vendor):
    # Create a new historical performance record
    HistoricalPerformance.objects.create(
        vendor=vendor,
        date=timezone.now(),
        on_time_delivery_rate=vendor.on_time_delivery_rate,
        quality_rating_avg=vendor.quality_rating_avg,
        average_response_time=vendor.average_response_time,
        fulfillment_rate=vendor.fulfillment_rate
    )