from django.shortcuts import render
from django.http import HttpResponse
from exam_reviews.models import exam_review, exam_review_store_data
# Create your views here.


from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import ExamReviewSerializer, ExamReviewStoreDataSerializer
from django.core.cache import cache
class ExamReviewAPIView(APIView):
    def get(self, request):
        # Try to get cached data
        cache_key = 'exam_reviews_list'
        cached_data = cache.get(cache_key)
        
        if cached_data is not None:
            return Response(cached_data)
            
        # If cache miss, get data from database
        exam_reviews = exam_review.objects.all()
        serializer = ExamReviewSerializer(exam_reviews, many=True)
        
        # Cache the response data for 15 minutes
        cache.set(cache_key, serializer.data, timeout=900)
        
        return Response(serializer.data)

class ExamReviewStoreDataAPIView(APIView):
    def get(self, request):
        exam_reviews_store_data = exam_review_store_data.objects.all()
        serializer = ExamReviewStoreDataSerializer(exam_reviews_store_data, many=True)
        return Response(serializer.data)
        
    def post(self, request):
        print("request.data",request.data)
        # Get the exam review instance
        # exam_review_id = request.data.get('exam_review_id')
        try:
            # exam_review_instance = exam_review.objects.get(id=exam_review_id)
            # Update request data with exam_review instance
            # data = request.data.copy()
            # data['exam_review'] = exam_review_id  # Just pass the ID since it's a foreign key
            
            serializer = ExamReviewStoreDataSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=201)
            return Response(serializer.errors, status=400)
        except exam_review.DoesNotExist:
            return Response({'error': 'Exam review not found'}, status=404)

def exam_review_page(request, url_slug):
    print("url_slug",url_slug)
    exam_review_name = url_slug.replace('-', ' ')
    exam_review_data = exam_review.objects.filter(button_name__iexact=exam_review_name).first()
    
    exam_shifts = list(range(1, exam_review_data.exam_shifts + 1))
    print("exam_shifts",exam_shifts)
    # if method is post
    submitted = False
    if request.method == 'POST':
        print("POST request")
        exam_day = request.POST.get('exam_day')
        exam_shift = request.POST.get('exam_shift')
        
        gender = request.POST.get('gender')
        
        category = request.POST.get('category')
        english_attempts = request.POST.get('english_attempts')
        
        maths_attempts = request.POST.get('maths_attempts')
        
        reasoning_attempts = request.POST.get('reasoning_attempts')
        
        gk_attempts = request.POST.get('gk_attempts')
        
        computer_attempts = request.POST.get('computer_attempts')
        
        exam_review_post = request.POST.get('exam_review')
        exam_review_store_data_save = exam_review_store_data(
            exam_review = exam_review_data,
            exam_day = exam_day,
            exam_shift = exam_shift,
            gender = gender,
            category = category,
            english_attempts = english_attempts,
            maths_attempts = maths_attempts,
            reasoning_attempts = reasoning_attempts,
            gk_attempts = gk_attempts,
            computer_attempts = computer_attempts,
            exam_review_data = exam_review_post,
        )
        exam_review_store_data_save.save()
        submitted = True
    
    return render(request, 'exam_review.html', {'exam_review': exam_review_data, 'exam_shifts': exam_shifts, 'submitted': submitted})

