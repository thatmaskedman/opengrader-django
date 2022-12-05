# from django.shortcuts import render
from .models import ExamGroup, Exam, KeyQuestion, KeySheet, Question
from rest_framework import viewsets
from rest_framework import views
# from rest_framework import permissions
# from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

from opengrader_backend.serializers import ( 
    ExamGroupSerializer, 
    GradedExamSerializer, 
    QuestionSerializer, 
    KeySheetSerializer, 
    KeyQuestionSerializer,
)


class FileUploadView(views.APIView):
    def put(self, request, filename, format=None):
        f = request.data['file']
        return Response(status=204)


class ExamGroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint of an Exam group
    """
    queryset = ExamGroup.objects.all()
    serializer_class = ExamGroupSerializer


class GradedExamViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows to be viewed or edited.
    """
    queryset = Exam.objects.all()
    serializer_class = GradedExamSerializer

    
class QuestionExamViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class KeySheetViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = KeySheet.objects.all()
    serializer_class = KeySheetSerializer


class KeyQuestionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = KeyQuestion.objects.all()
    serializer_class = KeyQuestionSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
