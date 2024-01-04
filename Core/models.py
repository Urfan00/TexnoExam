from django.db import models
from Account.models import Account
from Exam.models import Answer, Course, CourseTopic, Question
from services.mixins import DateMixin



class Group(DateMixin):
    name = models.CharField(max_length=100, unique=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_group')
    course_topic = models.ManyToManyField(CourseTopic, blank=True)
    is_active = models.BooleanField(default=True)
    exam_durations = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Group'
        verbose_name_plural = 'Group'


class AccountGroup(DateMixin):
    student = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='student_group')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='account_group')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.student.get_full_name()} - {self.group.name}"

    class Meta:
        verbose_name = 'Account Group'
        verbose_name_plural = 'Account Group'



class RandomQuestion(DateMixin):
    student = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='student_random_question')
    point_1_question = models.ManyToManyField(Question, related_name='point_1')
    point_2_question = models.ManyToManyField(Question, related_name='point_2')
    point_3_question = models.ManyToManyField(Question, related_name='point_3')
    status = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.student.get_full_name()} random questions"

    class Meta:
        verbose_name = 'Random Question'
        verbose_name_plural = 'Random Question'


class StudentAnswer(DateMixin):
    student = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='student_answer_question')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='student_question')
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='student_answer', null=True, blank=True)
    is_correct = models.BooleanField()

    def __str__(self):
        return f"{self.student.get_full_name()} answer"

    def save(self, *args, **kwargs):
        if self.answer and self.answer.is_correct:
            self.is_correct = True
        else:
            self.is_correct = False
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Student Answer'
        verbose_name_plural = 'Student Answer'

