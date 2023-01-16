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


class QuestionPostSerializer(serializers.ModelSerializer):
    response1 = ResponseSerializer()
    response2 = ResponseSerializer()

    class Meta:
        model = Question
        fields = ('question_text', 'response1', 'response2')
