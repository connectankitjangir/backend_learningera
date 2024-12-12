from django.shortcuts import render, redirect
from .models import Feedback,news_bar
from rest_framework.views import APIView
from django.core.cache import cache

# # Create your views here.
# def feedback(request):
#     if request.method == 'POST':
#         print('feedback submitted')
#         #save to database
#         Feedback.objects.create(
#             name=request.POST['name'],
#             email=request.POST['email'],
#             rating=request.POST['rating'],
#             comments=request.POST['comments']
#         )
#         return redirect('home')
#     return render(request, 'feedback.html')


from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializer import NewsBarSerializer, FeedbackSerializer

@api_view(['GET'])
def news_bar_list(request):
    # Try to get cached data
    cache_key = 'news_bar_list'
    cached_data = cache.get(cache_key)
    
    if cached_data is not None:
        return Response(cached_data)
        
    # If cache miss, get data from database
    news_bars = news_bar.objects.all().order_by('news_bar_order')
    serializer = NewsBarSerializer(news_bars, many=True)
    
    # Cache the response data for 15 minutes
    cache.set(cache_key, serializer.data, timeout=900)
    
    return Response(serializer.data)
@api_view(['GET', 'POST'])
def feedback_list(request):
    if request.method == 'POST':
        serializer = FeedbackSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
    feedbacks = Feedback.objects.all()
    serializer = FeedbackSerializer(feedbacks, many=True)
    return Response(serializer.data)

