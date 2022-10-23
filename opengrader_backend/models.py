from django.db import models

class ExamGroup(models.Model):
    avg_group_grade = models.FloatField()

class GradedExam(models.Model):
    name = models.CharField()
    name_blob = models.CharField()
    control_number = models.CharField()
    control_number_blob = models.CharField()
    key_letter = models.CharField()
    correct_answers = models.IntegerField()
    wrong_answers = models.IntegerField()
    grade = models.FloatField()
    exam_group = models.ForeignKey(ExamGroup, on_delete=models.CASCADE)

class Question(models.Model):
    graded_exam = models.ForeignKey(GradedExam, on_delete=models.CASCADE)
    number = models.CharField()
    chosen = models.CharField()
    filled = models.BooleanField()
    correct = models.BooleanField()

class KeyQuestion(models.Model):
    graded_exam = models.ForeignKey(ExamGroup, on_delete=models.CASCADE)
    key_class = models.CharField()
    number = models.CharField()
    answer = models.CharField()