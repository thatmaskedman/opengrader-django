import factory
from ...models import ExamGroup

class ExamGroupFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ExamGroup
        django_get_or_create = ('name',)

    name = factory.Faker('first_name')
    num_questions = 50
    date = '2023-01-01'