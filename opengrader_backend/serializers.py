# from django.contrib.auth.models import User
from .models import ExamGroup, Exam, KeySheet, Question, KeyQuestion, Student
from rest_framework import serializers
from rest_pandas import PandasSerializer
import pandas as pd


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


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'


class GradedExamSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Exam
        fields = (
            'id',
            'questions',
            'exam_group',
            'exam_image_original',
            'exam_image_graded',
            'key_sheet',
            'student',
            'name',
            'control_number',
            'file_uuid',
            'correct_answers',
            'wrong_answers',
            'grade',
            'is_graded',
        )


class QuestionPandasSerializer(PandasSerializer):
    def transform_dataframe(self, dataframe: pd.DataFrame):
        exam_dataframe = dataframe.pivot(index='number', columns='graded_exam')
        exam_dataframe = exam_dataframe.droplevel(level=0, axis=1)
        exam_dataframe['avg'] = exam_dataframe.mean(axis=1)
        return exam_dataframe


class GradePandasSerializer(PandasSerializer):
    def transform_dataframe(self, dataframe: pd.DataFrame):
        exam_dataframe = dataframe.pivot(index='number', columns='graded_exam')
        # exam_dataframe['avg'] = exam_dataframe.mean(axis=1)
        exam_dataframe = exam_dataframe.droplevel(level=0, axis=1)
        exam_dataframe = exam_dataframe.transpose()
        exam_dataframe['sum'] = exam_dataframe.sum(axis=1)
        return exam_dataframe


class ChosenPandasSerializer(PandasSerializer):
    def transform_dataframe(self, dataframe: pd.DataFrame):
        exam_dataframe = dataframe.pivot_table(index='number', columns='chosen', aggfunc=pd.Series.nunique, fill_value=0)
        exam_dataframe = exam_dataframe.droplevel(level=0, axis=1)
        return exam_dataframe


class ChosenDataFrameSerializer(serializers.ModelSerializer):
    graded_exam = serializers.SlugRelatedField(read_only=True, slug_field='name')
    class Meta:
        model = Question
        fields = (
            'graded_exam',
            'number',
            'chosen'
        )


class QuestionDataFrameSerializer(serializers.ModelSerializer):
    graded_exam = serializers.SlugRelatedField(read_only=True, slug_field='name')
    class Meta:
        model = Question
        fields = (
            'graded_exam',
            'number',
            'correct'
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