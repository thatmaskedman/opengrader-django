from django.contrib.auth.models import User
from .models import ExamGroup, GradedExam, KeySheet, Question, KeyQuestion
from rest_framework import serializers

class ExamGroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ExamGroup
        fields = ('name','avg_group_grade', 'date')


class GradedExamSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = GradedExam
        fields = (
            'name',
            'name_blob',
            'control_number',
            'control_number_blob',
            'correct_answers',
            'wrong_answers',
            'grade',
            'is_graded',
            'exam_group',
            'key_sheet'
        )


class QuestionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Question
        fields = (
            'graded_exam',
            'number',
            'chosen', 
            'filled', 
            'correct',
            'threshold',
        )

class KeyQuestionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = KeyQuestion
        fields = ('key_sheet','number', 'chosen')

class KeySheetSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = KeySheet
        fields = ('exam_group','key_class')