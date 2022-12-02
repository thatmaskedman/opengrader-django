import factory
from ...models import ExamGroup, KeySheet

class KeySheetFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = KeySheet
    
    exam_group = factory.Iterator(ExamGroup.objects.all())

class KeySheet(factory.django.DjangoModelFactory):
    class Meta:
        model = KeySheet
    key_class = 'a'
    exam_group = factory.Iterator(ExamGroup.objects.all())