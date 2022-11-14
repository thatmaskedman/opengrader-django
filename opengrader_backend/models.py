from django.db import models

LETTER_A = 'a'
LETTER_B = 'b'
LETTER_C = 'c'
LETTER_D = 'd'
LETTER_E = 'e'
LETTER_NONE = ''

CHOICES = [
    (LETTER_A, 'A'),
    (LETTER_B, 'B'),
    (LETTER_C, 'C'),
    (LETTER_D, 'D'),
    (LETTER_E, 'E'),
    (LETTER_NONE, 'Empty'),
]


class ExamGroup(models.Model):
    name = models.CharField(max_length=40)
    num_questions = models.IntegerField()
    avg_group_grade = models.FloatField(default=0.0)
    date = models.DateField()


class KeySheet(models.Model):
    exam_group = models.ForeignKey(ExamGroup, on_delete=models.CASCADE)
    key_class = models.CharField(
        max_length=1,
        choices=CHOICES,
        default=LETTER_NONE,
    )


class GradedExam(models.Model):
    exam_group = models.ForeignKey(ExamGroup, on_delete=models.CASCADE)
    key_sheet = models.ForeignKey(KeySheet, on_delete=models.CASCADE)
    STATES = [
        ('', 'Empty'),
        ('ambigous', 'Ambiguous'),
        ('review', 'Review'),
        ('graded ', 'Graded'),
    ]

    name = models.CharField(max_length=40)
    control_number = models.CharField(max_length=10)
    control_number_blob = models.BinaryField()
    state = models.CharField(
        max_length=10,
        choices=STATES,
        default='emtpy'
    )
    correct_answers = models.IntegerField(default=0)
    wrong_answers = models.IntegerField(default=0)
    is_graded = models.BooleanField(default=False)
    grade = models.FloatField(default=0.0)


class Question(models.Model):
    graded_exam = models.ForeignKey(GradedExam, related_name='questions', on_delete=models.CASCADE)
    num = models.IntegerField()
    chosen = models.CharField(
        max_length=1,
        choices=CHOICES,
        default=LETTER_NONE,
    )
    correct = models.BooleanField(default=False)
    threshold = models.FloatField(default=0.0)
    a_filled = models.BooleanField(default=False)
    b_filled = models.BooleanField(default=False)
    c_filled = models.BooleanField(default=False)
    d_filled = models.BooleanField(default=False)
    e_filled = models.BooleanField(default=False)

class KeyQuestion(models.Model):
    key_sheet = models.ForeignKey(KeySheet, related_name='key_questions', on_delete=models.CASCADE)
    number = models.IntegerField()
    chosen = models.CharField(
        max_length=1,
        choices=CHOICES,
        default=LETTER_NONE,
    )
    
    def __str__(self):
        return ''