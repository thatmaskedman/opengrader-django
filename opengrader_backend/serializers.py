from django.contrib.auth.models import User
from .models import ExamGroup, GradedExam, KeySheet, Question, KeyQuestion
from rest_framework import serializers


class ExamGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamGroup
        fields = '__all__'

class GradedExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = GradedExam
        fields = '__all__'

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'

class BulkKeyQuestionSerializer(serializers.ListSerializer):
    def create(self, validated_data):
        key_questions_data = [
            KeyQuestion(**item) for item in validated_data
        ]

        return KeyQuestion.objects.bulk_create(key_questions_data)

class KeyQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = KeyQuestion
        fields = '__all__'
        list_serializer_class = BulkKeyQuestionSerializer

class KeySheetSerializer(serializers.ModelSerializer):
    class Meta:
        model = KeySheet
        fields = '__all__'