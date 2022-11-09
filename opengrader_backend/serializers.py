from django.contrib.auth.models import User
from .models import ExamGroup, GradedExam, KeySheet, Question, KeyQuestion
from rest_framework import serializers


class ExamGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamGroup
        fields = (
            'id',
            'name',
            'avg_group_grade', 
            'date'
        )

class GradedExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = GradedExam
        fields = (
            'id',
            'name',
            'name_blob',
            'control_number',
            'correct_answers',
            'wrong_answers',
            'grade',
            'is_graded',
            'exam_group',
            'key_sheet'
        )

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = (
            'id',
            'graded_exam',
            'num',
            'chosen',
            'state', 
            'filled', 
            'correct',
            'threshold',
        )

class BulkKeyQuestionSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        key_questions_data = [
            KeyQuestion(**item) for item in validated_data
        ]

        return KeyQuestion.objects.bulk_create(key_questions_data)

class KeyQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = KeyQuestion
        fields = (
            'id',
            'key_sheet',
            'number', 
            'chosen'
        )
        list_serializer_class = BulkKeyQuestionSerializer

class KeySheetSerializer(serializers.ModelSerializer):
    class Meta:
        model = KeySheet
        fields = ('id', 'exam_group','key_class')