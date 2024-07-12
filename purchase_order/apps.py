from django.apps import AppConfig


class PurchaseOrderConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'purchase_order'
    
    def ready(self):
        import purchase_order.signals
