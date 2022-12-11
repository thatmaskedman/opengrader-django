import uuid
from django.db import models
from django.db.models.signals import pre_save
from django.core.files import File
from django.dispatch import receiver
from django.core.files.base import ContentFile

from opengradercv.cvprocessor import document, answersheet
import numpy as np
import cv2 as cv
import io

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

    def __str__(self):
        return self.name


class KeySheet(models.Model):
    exam_group = models.ForeignKey(ExamGroup, on_delete=models.CASCADE)
    key_class = models.CharField(
        max_length=1,
        choices=CHOICES,
        default=LETTER_NONE,
    )

    def __str__(self):
        return str(self.exam_group)


class Exam(models.Model):

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
    file_uuid = models.UUIDField(default=uuid.uuid4)
    state = models.CharField(
        max_length=10,
        choices=STATES,
        default='emtpy'
    )
    exam_image = models.FileField(upload_to='exams', default=None)
    correct_answers = models.IntegerField(default=0)
    wrong_answers = models.IntegerField(default=0)
    is_graded = models.BooleanField(default=False)
    grade = models.FloatField(default=0.0)
    
    def parse_questions(self):
        exam_bytes = io.BytesIO(self.exam_image.open(mode='rb').read())
        processor = document.DocumentProcessor(exam_bytes)
        processor.process()
        choice_points = processor.get_choice_points()
        intensities = processor.get_intensities()

        exam_group = ExamGroup.objects.get(pk=self.exam_group.pk)
        exam_parser = \
            answersheet.AnswerSheet(
                processor.img_scaled,
                choice_points, 
                thresholds=intensities,
                question_count=exam_group.num_questions,
                name=self.name,
                control_num=self.control_number)
        
        exam_parser.set_data()
        exam_parser.choose_answers()
        # self.exam_image.delete()

        # scaled_img_bytes = cv.imencode('.jpg', processor.img_scaled)
        # self
        # self.exam_image.save(
        #     f'{self.file_uuid}.jpg',
        #     ContentFile(bytes(scaled_img_bytes)),
        # )

        key_data = [
            {'number': k.number, 'chosen': k.chosen}
            for k in KeyQuestion.objects.filter(key_sheet=self.key_sheet)
        ]

        exam_parser.set_keydata(key_data)
        exam_parser.grade_data()

        graded_questions = [Question(graded_exam=self, **fields) for fields in exam_parser.question_data]

        Question.objects.bulk_create(graded_questions)

        exam_parser.mark_choices()
        _, graded_exam_nparray = cv.imencode('.jpg', exam_parser.img)
        
        self.exam_image.delete()
        self.exam_image.save(
            f'{self.file_uuid}.jpg',
            ContentFile(graded_exam_nparray.tobytes())
        )

    # Members.objects.all().order_by('firstname').values()
        # parsed_questions = [Question(**fields) for fields in exam_parser.question_data]
        # parsed_questions
    
    def set_choices(self):
        pass

    def grade(self):
        pass

    # def save(self, *args, **kwargs):
    #     # pre save
    #     super().save(*args, **kwargs)  # Call the "real" save() method.
    #     # post save
    #     exam_group = ExamGroup.objects.get(pk=self.exam_group.pk)
    #     Question.objects.bulk_create((
    #         Question(graded_exam=self, number=n)
    #         for n in range(1, exam_group.num_questions+1)))
    

    def __str__(self):
        return self.name

# @receiver(pre_save, sender=Exam)
# def grade_exam(sender, instance: Exam, **kwargs):
#     if instance.exam_image is not None:
#         exam_bytes = io.BytesIO((instance.exam_image.open(mode='rb').read()))

#         processor = document.DocumentProcessor(exam_bytes)
#         processor.process()
#         choice_points = processor.get_choice_points()
#         intensities = processor.get_intensities()

#         exam_group = ExamGroup.objects.get(pk=instance.exam_group.pk)
#         exam_parser = \
#             answersheet.AnswerSheet(
#                 processor.img_scaled,
#                 choice_points, 
#                 thresholds=intensities,
#                 question_count=exam_group.num_questions,
#                 name=instance.name,
#                 control_num=instance.control_number)
#         exam_parser.set_data()
#         exam_parser.choose_answers()
#         questions = Question.objects.filter(graded_exam=instance)
#         print(questions)
#                 # [Question(**fields) for fields in exam_parser.question_data]

#         # key_sheet = KeySheet.objects.get(pk=instance.key_sheet.pk)
#         # instance.
#         print(exam_parser.question_data)

class Question(models.Model):
    graded_exam = models.ForeignKey(
        Exam,
        related_name='questions', 
        on_delete=models.CASCADE)

    number = models.IntegerField()
    chosen = models.CharField(
        max_length=1,
        choices=CHOICES,
        default=LETTER_NONE,
    )
    correct = models.BooleanField(default=False)
    a_thresh = models.FloatField(default=0.0)
    b_thresh = models.FloatField(default=0.0)
    c_thresh = models.FloatField(default=0.0)
    d_thresh = models.FloatField(default=0.0)
    e_thresh = models.FloatField(default=0.0)
    a_filled = models.BooleanField(default=False)
    b_filled = models.BooleanField(default=False)
    c_filled = models.BooleanField(default=False)
    d_filled = models.BooleanField(default=False)
    e_filled = models.BooleanField(default=False)


class KeyQuestion(models.Model):
    key_sheet = models.ForeignKey(
        KeySheet,
        related_name='key_questions',
        on_delete=models.CASCADE)

    number = models.IntegerField()
    chosen = models.CharField(
        max_length=1,
        choices=CHOICES,
        default=LETTER_NONE,
    )

    def __str__(self):
        return ''
