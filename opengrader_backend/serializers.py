from django.contrib.auth.models import User
from .models import ExamGroup, GradedExam, KeySheet, Question, KeyQuestion
from rest_framework import serializers


class ExamGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamGroup
        fields = '__all__'



class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'
        
class GradedExamSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)
    
    class Meta:
        model = GradedExam
        fields = (
            'id',
            'questions',
            'exam_group',
            'key_sheet', 
            'name',
            'control_number',
            'control_number_blob',
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
    class Meta:
        model = KeySheet
        fields = '__all__'