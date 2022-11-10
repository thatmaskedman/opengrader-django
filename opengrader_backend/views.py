from django.shortcuts import render
from .models import ExamGroup, GradedExam, KeyQuestion, KeySheet, Question
from rest_framework import viewsets
from rest_framework import views
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status

from opengrader_backend.serializers import ( 
    ExamGroupSerializer, 
    GradedExamSerializer, 
    QuestionSerializer, 
    KeySheetSerializer, 
    KeyQuestionSerializer
)

class FileUploadView(views.APIView):
    def put(self, request, filename, format=None):
        f = request.data['file']
        return Response(status=204)


class ExamGroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = ExamGroup.objects.all()
    serializer_class = ExamGroupSerializer


class GradedExamViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows to be viewed or edited.
    """
    queryset = GradedExam.objects.all()
    serializer_class = GradedExamSerializer

    
class QuestionExamViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


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