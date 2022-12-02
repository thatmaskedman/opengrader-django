import factory
import faker
from ...models import ExamGroup, Exam, Question, KeySheet

class ExamFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Exam
        django_get_or_create = ('name',)
    name = name = factory.Faker('first_name')
    exam_group = factory.Iterator(ExamGroup.objects.all())
    key_sheet = factory.Iterator(KeySheet.objects.all())
    control_number = '17330462'

class QuestionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Question
    
    exam = factory.SubFactory(ExamFactory)