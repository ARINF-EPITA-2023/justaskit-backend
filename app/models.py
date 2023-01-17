import json
import pickle
from datetime import datetime

from django.db import models


class Response:
    response_text: str
    choice: int

    def __init__(self, response_text, choice=0):
        self.response_text = response_text
        self.choice = choice

    def to_dict(self):
        return {
            'response_text': self.response_text,
            'choice': self.choice
        }

    def to_json(self):
        return json.dumps(self.to_dict())

    @staticmethod
    def from_json(json_dct):
        return Response(json_dct['response_text'], json_dct['choice'])

    def __str__(self):
        return self.response_text


class Question:
    id: str
    question_text: str
    response1: Response
    response2: Response
    upvote = 0
    downvote = 0

    def __init__(self, question_text, response1, response2, id=0, upvote=0, downvote=0):
        self.question_text = question_text
        self.response1 = response1
        self.response2 = response2
        self.id = id
        self.upvote = upvote
        self.downvote = downvote

    def __str__(self):
        return self.question_text

    def to_json(self):
        return json.dumps(self.to_dict())

    def to_dict(self):
        return {
            'id': self.id.__str__(),
            'question_text': self.question_text,
            'response1': self.response1.to_dict(),
            'response2': self.response2.to_dict(),
            'upvote': self.upvote,
            'downvote': self.downvote
        }

    @staticmethod
    def from_json(json_dct):
        response1 = Response.from_json(json_dct['response1'])
        response2 = Response.from_json(json_dct['response2'])
        upvote = int(json_dct['upvote'])
        downvote = int(json_dct['downvote'])
        id = json_dct['id']
        question_text = json_dct['question_text']
        return Question(question_text, response1, response2, id, upvote, downvote)
