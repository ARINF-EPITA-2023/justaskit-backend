# Create your views here.
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.schemas.openapi import AutoSchema
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from .models import Question, Response
from .serializers import QuestionSerializer, ResponseSerializer, QuestionPostSerializer


class QuestionList(ListCreateAPIView):
    def get_serializer_class(self):
        if self.request.data is not None:
            return QuestionPostSerializer
        else:
            return QuestionSerializer

    def create(self, request, *args, **kwargs):
        serializer = QuestionPostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    queryset = Question.objects.order_by('?')

    schema = AutoSchema(tags=['Questions'])


class QuestionDetail(ModelViewSet):

    @action(detail=True, methods=['get'])
    def get(self, request, pk):
        question = Question.objects.get(pk=pk)
        serializer = QuestionSerializer(question)
        return Response(serializer.data)

    @action(detail=True, methods=['put'])
    def put(self, request, pk):
        question = Question.objects.get(pk=pk)
        serializer = QuestionSerializer(question, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['delete'])
    def delete(self, request, pk):
        question = Question.objects.get(pk=pk)
        question.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    queryset = Question.objects.all()
    schema = AutoSchema(tags=['Questions'])
    serializer_class = QuestionSerializer


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
