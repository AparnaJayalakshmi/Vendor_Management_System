from rest_framework import serializers
from .models import PurchaseOrder
from django.utils import timezone
import json

class PurchaseOrderSerializer(serializers.ModelSerializer):
    po_number = serializers.CharField(read_only=True)
    order_date = serializers.DateTimeField(format="%d-%B-%Y", required=False)
    delivery_date = serializers.DateTimeField(format="%d-%B-%Y", required=False)

    class Meta:
        model = PurchaseOrder
        fields = '__all__'


    def create(self, validated_data):
        # Set order_date to the current date if not provided
        validated_data.setdefault('order_date', timezone.now())
        
        # Calculate delivery date as 7 days from the order date
        validated_data['delivery_date'] = validated_data['order_date'] + timezone.timedelta(days=7)

        validated_data['issue_date'] = validated_data['order_date']
        
        last_po_number = PurchaseOrder.objects.all().order_by('id').last()
        if not last_po_number:
            validated_data['po_number'] = 'P001'
        else:
            po_number = 'P' + str(last_po_number.id + 1).zfill(3)
            validated_data['po_number'] = po_number

       # Parse the items field and calculate the quantity
        items = validated_data.get('items', '[]')
        if isinstance(items, str):
            items = json.loads(items)
        
        quantity = 0
        for item in items:
            item_quantity = item.get('quantity', 0)
            quantity += item_quantity

        validated_data['quantity'] = quantity

        return super().create(validated_data)

    def validate_quality_rating(self,value):
        current_status = self.instance.status
        if current_status.lower() != 'completed':
            raise serializers.ValidationError('Cannot give Quality rating ')
        if value not in range(1,11):
            raise serializers.ValidationError('Quality Rating must between 1-10')
        
        return value