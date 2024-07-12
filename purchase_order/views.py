from django.shortcuts import render
from .models import PurchaseOrder
from .serializers import PurchaseOrderSerializer
from rest_framework import status,viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

# Create your views here.
class PurchaseOrderViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        vendor_id = self.request.query_params.get('vendor_id')
        if vendor_id:
            queryset = queryset.filter(vendor_id=vendor_id)
        return queryset

    @action(detail=True,  methods=['get'])
    def acknowledge(self, request, pk=None):
        try:
            purchase_order = self.get_object()

            # Set acknowledgment date to the current time
            purchase_order.acknowledgment_date = timezone.now()
            purchase_order.save()

            return Response({'status': 'acknowledged'}, status=status.HTTP_200_OK)
        except PurchaseOrder.DoesNotExist:
            return Response({'error': 'PurchaseOrder not found'}, status=status.HTTP_404_NOT_FOUND)
