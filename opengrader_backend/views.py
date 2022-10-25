from django.shortcuts import render
from .models import ExamGroup, GradedExam
from rest_framework import viewsets
from rest_framework import permissions
from opengrader_backend.serializers import ExamGroupSerializer, GradedExamSerializer 

class ExamGroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = ExamGroup.objects.all()
    serializer_class = ExamGroupSerializer


class GradedExamViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = GradedExam.objects.all()
    serializer_class = GradedExamSerializer