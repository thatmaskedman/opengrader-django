from django.contrib.auth.models import User
from .models import ExamGroup, GradedExam, Question, KeyQuestion
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
            'key_letter',
            'correct_answers',
            'wrong_answers',
            'grade',
            'exam_group',
        )


class QuestionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Question
        fields = (
            'graded_exam',
            'chosen', 
            'filled', 
            'correct',
            'threshold',
        )


# class KeyQuestion(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = KeyQuestion
#         fields = ('name','avg_group_grade', 'date')