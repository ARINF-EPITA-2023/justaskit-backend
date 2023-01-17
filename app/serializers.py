import json
import pickle
from datetime import datetime

from rest_framework import serializers

from .models import Question, Response


class ResponseSerializer:
    response_text: str
    choice: int

    def __init__(self, response_text, choice=0):
        self.response_text = response_text
        self.choice = choice


class QuestionSerializer:
    id: int
    question_text: str
    pub_date: datetime
    response1: ResponseSerializer
    response2: ResponseSerializer
    upvote: int
    downvote: int

    def __init__(self, question_text, response1, response2, id=0, upvote=0, downvote=0):
        self.question_text = question_text
        self.response1 = response1
        self.response2 = response2
        self.id = id
        self.upvote = upvote
        self.downvote = downvote

    @staticmethod
    def from_json(json_dct):
        return QuestionSerializer(json_dct['question_text'], json_dct['response1'], json_dct['response2'], json_dct['id'], int(json_dct['upvote']), int(json_dct['downvote']))

    def to_model(self):
        return Question(self.question_text, Response(self.response1['response_text'], self.response1['choice']),
                        Response(self.response2['response_text'], self.response2['choice']), self.id, self.upvote, self.downvote)


class ResponsePostSerializer:
    response_text: str

    def __init__(self, response_text):
        self.response_text = response_text


class QuestionPostSerializer:
    question_text: str
    response1: ResponsePostSerializer
    response2: ResponsePostSerializer

    def __init__(self, question_text, response1, response2):
        self.question_text = question_text
        self.response1 = response1
        self.response2 = response2

    @staticmethod
    def from_json(json_dct):
        return QuestionPostSerializer(json_dct['question_text'], ResponsePostSerializer(json_dct['response1']['response_text']),
                                      ResponsePostSerializer(json_dct['response2']['response_text']))

    def to_model(self):
        return Question(self.question_text, Response(self.response1.response_text), Response(self.response2.response_text))
