from rest_framework import serializers

from .models import Question, Response


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('id', 'question_text', 'pub_date', 'response1', 'response2', 'upvotes', 'downvotes')


class ResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Response
        fields = ('id', 'response_text', 'choices')
