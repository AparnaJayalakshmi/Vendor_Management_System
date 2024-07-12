from rest_framework import viewsets,status
from .serializers import VendorSerializer,HistoricalPerformanceSerializer
from .models import Vendor,HistoricalPerformance
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

# Create your views here.
class VendorModelViewset(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

    @action(detail=True, methods=['get'], url_path='performance')
    def performance(self, request, pk=None):
        try:
            vendor = self.get_object()
        except Vendor.DoesNotExist:
            return Response({'error': 'Vendor not found'}, status=status.HTTP_404_NOT_FOUND)

        performance_data = {
            'on_time_delivery_rate': vendor.on_time_delivery_rate,
            'quality_rating_avg': vendor.quality_rating_avg,
            'average_response_time': vendor.average_response_time,
            'fulfillment_rate': vendor.fulfillment_rate,
        }

        return Response(performance_data, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['get'], url_path='performance-history')
    def performance_history(self, request, pk=None):
        try:
            vendor = self.get_object()
            performance_data = HistoricalPerformance.objects.filter(vendor=vendor)
            serializer = HistoricalPerformanceSerializer(performance_data, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Vendor.DoesNotExist:
            return Response({'error': 'Vendor not found'}, status=status.HTTP_404_NOT_FOUND)
