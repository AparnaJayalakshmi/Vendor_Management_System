from rest_framework import serializers
from django.utils import timezone
from .models import Vendor,HistoricalPerformance
import json

class VendorSerializer(serializers.ModelSerializer):
    vendor_code = serializers.CharField(read_only=True)

    class Meta:
        model = Vendor
        fields = '__all__'

    def create(self, validated_data):
        last_vendor = Vendor.objects.all().order_by('id').last()
        if not last_vendor:
            validated_data['vendor_code'] = 'V001'
        else:
            last_vendor_code = last_vendor.vendor_code
            last_code_number = int(last_vendor_code[1:])  # Get the numeric part of the last vendor code
            new_code_number = last_code_number + 1
            new_vendor_code = 'V' + str(new_code_number).zfill(3)
            validated_data['vendor_code'] = new_vendor_code

        return Vendor.objects.create(**validated_data)
    
class HistoricalPerformanceSerializer(serializers.ModelSerializer):
    # date = serializers.DateTimeField(format="%d-%B-%Y %H:%M:%S")
    date = serializers.DateTimeField(format="%d-%B-%Y %I:%M %p")

    class Meta:
        model = HistoricalPerformance
        fields = '__all__'
    
    
