from django.http import Http404, HttpResponse
from django.shortcuts import render
from airport.models import *
from rest_framework.response import Response
from rest_framework.views import APIView
from airport.serializers import *
from airport.paginations import CustomPagination


class AirportView(APIView):
    pagination_class = CustomPagination

    def get(self, request):
        airports = Airport.objects.all()
        paginator = CustomPagination()
        result_page = paginator.paginate_queryset(airports, request)
        serializer = AirportSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
    
    def post(self, request):
        serializer = AirportSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
class AirportDetailedView(APIView):
    pagination_class = CustomPagination

    def get_object(self, pk):
        try:
            return Airport.objects.get(pk=pk)
        except Airport.DoesNotExist:
            raise Http404
        
    def get(self, request, pk=None):
        if pk:
            airport = self.get_object(pk)
            serializer = AirportSerializer(airport)
            return Response(serializer.data)
        else:
            airports = Airport.objects.all()
            paginator = CustomPagination()
            result_page = paginator.paginate_queryset(airports, request)
            serializer = AirportSerializer(result_page, many=True)
            return paginator.get_paginated_response(serializer.data)
    
    def put(self, request, pk):
        airport = self.get_object(pk)
        serializer = AirportSerializer(airport, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
    def delete(self, request, pk):
        airport = self.get_object(pk)
        airport.is_active = False
        airport.save()
        return HttpResponse(status=204)
    
