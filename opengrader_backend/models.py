from unittest.util import _MAX_LENGTH
from django.db import models

class ExamGroup(models.Model):
    name = models.CharField(max_length=40)
    avg_group_grade = models.FloatField()
    date = models.DateField()

class GradedExam(models.Model):
    name = models.CharField(max_length=40)
    name_blob = models.BinaryField()
    control_number = models.CharField(max_length=10)
    control_number_blob = models.BinaryField()
    key_letter = models.CharField(max_length=1)
    correct_answers = models.IntegerField()
    wrong_answers = models.IntegerField()
    grade = models.FloatField()
    exam_group = models.ForeignKey(ExamGroup, on_delete=models.CASCADE)

class Question(models.Model):
    graded_exam = models.ForeignKey(GradedExam, on_delete=models.CASCADE)
    number = models.CharField(max_length=3)
    chosen = models.CharField(max_length=1)
    filled = models.BooleanField()
    correct = models.BooleanField()
    threshold = models.FloatField()

class KeyQuestion(models.Model):
    graded_exam = models.ForeignKey(ExamGroup, on_delete=models.CASCADE)
    key_class = models.CharField(max_length=1)
    number = models.CharField(max_length=3)
    choice = models.CharField(max_length=1)