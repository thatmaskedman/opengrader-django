from django.contrib.auth.models import User
from .models import ExamGroup, GradedExam, Question, KeyQuestion
from rest_framework import serializers

class ExamGroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ExamGroup
        fields = ['avg_group_grade', 'date']


class GradedExamSerializer(serializers.HyperlinkedModelSerializer):
    pass


class QuestionSerializer(serializers.HyperlinkedModelSerializer):
    pass


class KeyQuestion(serializers.HyperlinkedModelSerializer):
    pass

