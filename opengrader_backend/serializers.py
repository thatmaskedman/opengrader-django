# from django.contrib.auth.models import User
from .models import ExamGroup, Exam, KeySheet, Question, KeyQuestion
from rest_framework import serializers
# from rest_framework import generics


class ExamGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamGroup
        fields = '__all__'


class BulkQuestionSerializer(serializers.ListSerializer):
    def create(self, validated_data):
        questions_data = [
            Question(**item) for item in validated_data
        ]

        return Question.objects.bulk_create(questions_data)


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'
        list_serializer_class = BulkQuestionSerializer


class GradedExamSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Exam
        fields = (
            'id',
            'questions',
            'exam_group',
            'exam_image',
            'key_sheet',
            'name',
            'control_number',
            'file_uuid',
            'correct_answers',
            'wrong_answers',
            'is_graded',
        )


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
    key_questions = KeyQuestionSerializer(many=True, read_only=True)
   
    class Meta:
        model = KeySheet
        fields = '__all__'