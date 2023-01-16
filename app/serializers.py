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


class ResponsePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Response
        fields = ['response_text']


class QuestionPostSerializer(serializers.ModelSerializer):
    response1 = ResponsePostSerializer()
    response2 = ResponsePostSerializer()

    class Meta:
        model = Question
        fields = ('question_text', 'response1', 'response2')

    def create(self, validated_data):
        nested_data = validated_data.pop('response1')
        nested_obj = Response.objects.create(**nested_data)

        nested_data = validated_data.pop('response2')
        nested_obj = Response.objects.create(**nested_data)

        question = Question.objects.create(nested_field=nested_obj, **validated_data)
        return question
