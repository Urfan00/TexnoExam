from django.shortcuts import redirect, render
from django.views.generic import ListView
from Account.models import Account
from Core.models import AccountGroup, RandomQuestion, StudentAnswer
from .models import Answer, Question



class RuleView(ListView):
    model = Account
    template_name = 'quiz-rule.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["student"] = Account.objects.filter(username=self.request.user.username).first()

        if not RandomQuestion.objects.filter(student=self.request.user, status=True).exists():
            account_group = AccountGroup.objects.filter(student=self.request.user, is_active=True).first()

            if account_group.group.is_active:
                group_course_topics = account_group.group.course_topic.all()

                one_point = Question.objects.filter(course_topic__in=group_course_topics, point=1, is_active=True).order_by('?')[:3]
                two_point = Question.objects.filter(course_topic__in=group_course_topics, point=2, is_active=True).order_by('?')[:4]
                three_point = Question.objects.filter(course_topic__in=group_course_topics, point=3, is_active=True).order_by('?')[:3]

                random_questions = RandomQuestion.objects.create(student=self.request.user)

                random_questions.point_1_question.set(one_point)
                random_questions.point_2_question.set(two_point)
                random_questions.point_3_question.set(three_point)

        return context



class QuizView(ListView):
    model = RandomQuestion
    template_name = 'dshb-quiz.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["student_questions"] = RandomQuestion.objects.filter(student=self.request.user, status=True).first()
        return context

    def post(self, request, *args, **kwargs):
        # Process the submitted form data and save student answers
        student_random_questions = RandomQuestion.objects.filter(student=request.user, status=True).first()

        for question in student_random_questions.point_1_question.all():
            answer_id = request.POST.get(f'question_{question.id}')
            if answer_id and answer_id.isdigit() and Answer.objects.filter(id=answer_id).exists():
                answer = question.question_answer.get(id=answer_id)
                StudentAnswer.objects.create(student=request.user, question=question, answer=answer)
            else:
                StudentAnswer.objects.create(student=request.user, question=question)

        for question in student_random_questions.point_2_question.all():
            answer_id = request.POST.get(f'question_{question.id}')
            if answer_id and answer_id.isdigit() and Answer.objects.filter(id=answer_id).exists():
                answer = question.question_answer.get(id=answer_id)
                StudentAnswer.objects.create(student=request.user, question=question, answer=answer)
            else:
                StudentAnswer.objects.create(student=request.user, question=question)

        for question in student_random_questions.point_3_question.all():
            answer_id = request.POST.get(f'question_{question.id}')
            if answer_id and answer_id.isdigit() and Answer.objects.filter(id=answer_id).exists():
                answer = question.question_answer.get(id=answer_id)
                StudentAnswer.objects.create(student=request.user, question=question, answer=answer)
            else:
                StudentAnswer.objects.create(student=request.user, question=question)

        return redirect('index')