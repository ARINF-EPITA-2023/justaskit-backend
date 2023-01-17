# Create your views here.
import json
import os
import random
import uuid

import redis
from django.http import JsonResponse
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_204_NO_CONTENT
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from .models import Question
from .serializers import QuestionPostSerializer, QuestionSerializer


class QuestionList(APIView):
    redis_instance = redis.StrictRedis(host=os.environ.get('REDIS_HOST'), port=int(os.environ.get('REDIS_PORT')), password=os.environ.get('REDIS_PASSWORD'), db=0)

    def post(self, request, *args, **kwargs):
        question = QuestionPostSerializer.from_json(request.data).to_model()
        question.id = uuid.uuid4().__str__()
        self.redis_instance.set(question.id, question.to_json())
        return JsonResponse(data=question.to_dict(), status=HTTP_200_OK)

    def get(self, request, format=None):
        questions = []
        for key in self.redis_instance.keys("*"):
            json_dct = json.loads(self.redis_instance.get(key))
            question = Question.from_json(json_dct)
            questions.append(question)
        random.shuffle(questions)
        data = [question.to_dict() for question in questions]
        return JsonResponse(data=data, status=HTTP_200_OK, safe=False)


class QuestionDetail(APIView):
    redis_instance = redis.StrictRedis(host=os.environ.get('REDIS_HOST'), port=int(os.environ.get('REDIS_PORT')), password=os.environ.get('REDIS_PASSWORD'), db=0)

    @action(detail=True, methods=['get'])
    def get(self, request, pk):
        json_dct = json.loads(self.redis_instance.get(pk))
        question = Question.from_json(json_dct).to_dict()
        return JsonResponse(data=question, status=HTTP_200_OK, safe=False)

    @action(detail=True, methods=['put'])
    def put(self, request, pk):
        question = self.redis_instance.exists(pk)
        if question:
            question = QuestionSerializer.from_json(request.data).to_model()
            self.redis_instance.set(pk, question.to_json())
        return JsonResponse(data=request.data, status=HTTP_200_OK, safe=False)

    @action(detail=True, methods=['delete'])
    def delete(self, request, pk):
        self.redis_instance.delete(pk)
        return Response(HTTP_204_NO_CONTENT)


class HelloView(APIView):
    @action(detail=True, methods=['get'])
    def get(self, request):
        return Response(data="Hello World!", status=HTTP_200_OK)
