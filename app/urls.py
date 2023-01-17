from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from rest_framework.schemas import get_schema_view

from app.views import QuestionList, QuestionDetail, HelloView

urlpatterns = [
    path('hello/', HelloView.as_view()),
    path('questions', QuestionList.as_view(), name='questions'),
    path('questions/<str:pk>',
         csrf_exempt(QuestionDetail.as_view()),
         name='question detail'),

]
