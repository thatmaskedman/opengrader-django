from django.test import TestCase
from .factories.examgroup import ExamGroupFactory
from .factories.keysheet import KeySheetFactory
from .factories.exam import ExamFactory

from ..models import ExamGroup, Exam, KeySheet

class ExamGroupTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        ExamGroupFactory.create_batch(10)

    def test_foo(self):
        print(ExamGroup.objects.all())

class ExamTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        ExamGroupFactory.create()
        KeySheetFactory.create()        
        ExamFactory.create_batch(10)


    def test_foo(self):
        print(Exam.objects.all())