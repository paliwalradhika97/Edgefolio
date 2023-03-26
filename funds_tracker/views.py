from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Fund
from .serializers import FundSerializer, UploadSerializer
from .renderers import CSVRenderer
from django.http import Http404
from django.shortcuts import render
from django.db.models import Sum

class FundAPI(APIView):
    renderer_classes = [CSVRenderer]
    def get(self, request):     
        strategy = request.GET.get("strategy")  
        funds = Fund.objects.all()
        if strategy:
            funds = funds.filter(strategy=strategy)
        
        funds_sum = funds.aggregate(Sum('aum')) 
     
        serializer = FundSerializer(funds, many=True)
        return Response({"data":serializer.data, "funds_sum":str(funds_sum["aum__sum"])})

    def post(self, request, format=None):
        serializer = UploadSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": "Successfully Uploaded"}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FundObjectAPI(APIView):
    def get_object(self, pk):
        try:
            return Fund.objects.get(pk=pk)
        except Fund.DoesNotExist:
            raise Http404
        
    def get(self, request, pk):    
        funds = self.get_object(pk)
        serializer = FundSerializer(funds, many=False)
        return Response(serializer.data)

def home(request):
    return render(request, "homepage.html")
 

 