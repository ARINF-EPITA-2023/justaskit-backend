from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from rest_framework.decorators import action
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.schemas.openapi import AutoSchema
from rest_framework.viewsets import ModelViewSet

from .models import Question, Response
from .serializers import QuestionSerializer, ResponseSerializer


class QuestionList(ListCreateAPIView):
    queryset = Question.objects.order_by('?')
    serializer_class = QuestionSerializer
    schema = AutoSchema(tags=['Questions'])


class QuestionDetail(ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    schema = AutoSchema(tags=['Questions'])


class ResponseDetail(ModelViewSet):
    @action(detail=True, methods=['put'])
    def updateChoices(self, request, pk):
        response = Response.objects.get(pk=pk)
        response.choices = request.data['choices']
        response.save()
        return Response(response)

    queryset = Response.objects.all()
    serializer_class = ResponseSerializer
    schema = AutoSchema(tags=['Responses'])
