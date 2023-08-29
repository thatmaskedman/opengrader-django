# from django.shortcuts import render
import io
import pandas as pd
from .models import ExamGroup, Exam, KeyQuestion, KeySheet, Question, Student
from rest_pandas import PandasView
from rest_framework import viewsets
from rest_framework import views
from rest_framework import renderers

from rest_framework.decorators import parser_classes
from rest_framework.parsers import MultiPartParser, FileUploadParser
# from rest_framework import permissions
# from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import action

from rest_framework import status

from opengrader_backend.serializers import (
    ChosenDataFrameSerializer,
    ChosenPandasSerializer,
    ExamGroupSerializer,
    GradePandasSerializer,
    GradedExamSerializer,
    QuestionDataFrameSerializer,
    QuestionPandasSerializer,
    QuestionSerializer,
    KeySheetSerializer,
    KeyQuestionSerializer,
    StudentSerializer,
)


class ExamUploadView(views.APIView):
    def put(self, request, filename, format=None):
        f = request.data['file']
        print(request.query_params)
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

    def get_queryset(self):
        queryset = Exam.objects.all()
        examgroup_pk = self.request.query_params.get('examgroup')
        if examgroup_pk is not None:
            examgroup = ExamGroup.objects.filter(pk=examgroup_pk).first()
            queryset = queryset.filter(exam_group=examgroup)
        
        return queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    @action(detail=True, methods=['put'], name='Grade Current Exam')
    def grade(self, request, pk=None):
        exam: Exam = self.get_object()
        serializer: GradedExamSerializer = self.get_serializer()
        headers = self.get_success_headers(serializer.data)

        try: 
            exam.parse_questions()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED, headers=headers)
        
        except ValueError:
            return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST, headers=headers)
    

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

    def get_queryset(self):
        queryset = KeySheet.objects.all()
        examgroup_pk = self.request.query_params.get('examgroup')
        if examgroup_pk is not None:
            examgroup = ExamGroup.objects.filter(pk=examgroup_pk).first()
            queryset = queryset.filter(exam_group=examgroup).order_by('key_class')
        
        return queryset
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        
        keysheet_id = serializer.data['id']
        keysheet = KeySheet.objects.filter(id=keysheet_id).first()
        
        num_questions = \
            ExamGroup.objects.filter(pk=keysheet.exam_group.id).first().num_questions
        
        KeyQuestion.objects.bulk_create([
            KeyQuestion(number=n, key_sheet=keysheet, chosen='a')
            for n in range(1, num_questions+1)
        ])
        
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    # @action(detail=True, methods=['post'], name='Initialize Fields')
    # def init(self, request, pk=None):
    #     keysheet: KeySheet = self.get_object()
    #     serializer: GradedExamSerializer = self.get_serializer()
    #     headers = self.get_success_headers(serializer.data)

    #     try: 
    #         keysheet.initialize()
    #         return Response(serializer.data, status=status.HTTP_202_ACCEPTED, headers=headers)
        
    #     except ValueError:
    #         return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST, headers=headers)
        

class StudentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def get_queryset(self):
        queryset = Student.objects.all()
        examgroup_pk = self.request.query_params.get('examgroup')
        if examgroup_pk is not None:
            examgroup = ExamGroup.objects.filter(pk=examgroup_pk).first()
            queryset = queryset.filter(exam_group=examgroup)
        
        return queryset


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


class ExamDataView(PandasView):
    queryset = Question.objects.none()

    def get_queryset(self): 
        examgroup_pk = self.kwargs['examgroup']
        examgroup = ExamGroup.objects.get(pk=examgroup_pk)
        exams = Exam.objects.filter(exam_group=examgroup)
        return Question.objects.filter(graded_exam__in=exams)

    serializer_class = QuestionDataFrameSerializer
    pandas_serializer_class = QuestionPandasSerializer


class ChosenDataView(PandasView):
    queryset = Question.objects.none()

    def get_queryset(self): 
        examgroup_pk = self.kwargs['examgroup']
        keysheet = KeySheet.objects.get(pk=examgroup_pk)
        exams = Exam.objects.filter(key_sheet=keysheet)
        return Question.objects.filter(graded_exam__in=exams)


    serializer_class = ChosenDataFrameSerializer
    pandas_serializer_class = ChosenPandasSerializer


class GradedDataView(PandasView):
    queryset = Question.objects.none()

    def get_queryset(self): 
        examgroup_pk = self.kwargs['examgroup']
        examgroup = ExamGroup.objects.get(pk=examgroup_pk)
        exams = Exam.objects.filter(exam_group=examgroup)
        return Question.objects.filter(graded_exam__in=exams)

    serializer_class = QuestionDataFrameSerializer
    pandas_serializer_class = GradePandasSerializer


class JPEGRenderer(renderers.BaseRenderer):
    media_type = 'image/jpeg'
    format = 'jpg'
    charset = None
    render_style = 'binary'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        return data


class PreviewView(views.APIView):
    parser_classes = [MultiPartParser]
    renderer_classes = [JPEGRenderer]

    def post(self, request, format='image/*'):
        image = request.data['file']
        try: 
            image_preview = Exam.preview_boxes(image)
            return Response(image_preview, status=status.HTTP_202_ACCEPTED, content_type='image/jpeg')
        
        except ValueError:
            return Response(status=status.HTTP_400_BAD_REQUEST) 


class FileUploadView(views.APIView):
    parser_classes = [MultiPartParser]

    def post(self, request, format=None):
        file_obj = request.data['file']
        exam_group_pk = request.data['examgroup']
        df = pd.read_excel(file_obj)
        print(df)
        Student.objects.bulk_create((
            Student(name=row['name'], control_number=row['control_num'], exam_group=ExamGroup(pk=exam_group_pk))
            for _, row in df.iterrows()
        ))

        return Response(status=204)