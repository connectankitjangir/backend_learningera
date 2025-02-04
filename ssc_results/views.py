from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import SSCResult
from .serializers import SSCResultSerializer


class SSCResultPostView(APIView):
    def post(self, request):
        roll_number = request.data.get("roll_number")  # Get roll_number from request
        
        if not roll_number:
            return Response({"error": "roll_number is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Fetch candidate data from SQLite
            result = SSCResult.objects.using('ssc_results_db').get(roll_number=roll_number)
            serializer = SSCResultSerializer(result)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except SSCResult.DoesNotExist:
            print("Result not found")
            return Response({"error": "Result not found"}, status=status.HTTP_404_NOT_FOUND)





