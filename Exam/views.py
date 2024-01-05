from django.shortcuts import redirect, render
from django.views.generic import ListView
from Account.models import Account, StudentResult
from Core.models import AccountGroup, RandomQuestion, StudentAnswer
from .models import Answer, Question
from django.db.models import F
from django.http import Http404, HttpResponseForbidden



class AuthUserStatusMixin:
    def dispatch(self, request, *args, **kwargs):
        # Check if the user is authenticated
        if request.user.is_authenticated:
            # Check if the user is not staff or not superuser
            if not (request.user.is_staff or request.user.is_superuser):
                # Check if user status is true
                if request.user.status:
                    return super().dispatch(request, *args, **kwargs)
                else:
                    # User status is false, redirect with a warning
                    return render(request, '404.html')
            else:
                # User is staff or superuser, redirect to 404 page
                return render(request, '404.html')
        else:
            # User is not authenticated, redirect to login page or any other page as needed
            return redirect('login')  # Change 'login' to the actual login page URL



class RuleView(AuthUserStatusMixin, ListView):
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


class QuizView(AuthUserStatusMixin, ListView):
    model = RandomQuestion
    template_name = 'dshb-quiz.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["student_questions"] = RandomQuestion.objects.filter(student=self.request.user, status=True).first()
        endTime = AccountGroup.objects.filter(student=self.request.user, is_active=True).first()
        context['endTime'] = endTime.group.end_time

        return context

    def post(self, request, *args, **kwargs):
        # Process the submitted form data and save student answers
        student_random_questions = RandomQuestion.objects.filter(student=self.request.user, status=True).first()

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

        # Calculate points
        student_answers = list(StudentAnswer.objects.filter(student=self.request.user).order_by('-created_at')[:10])

        point_1_points = sum(1 for answer in student_answers if answer.question.point == 1 and answer.is_correct)
        point_2_points = sum(1 for answer in student_answers if answer.question.point == 2 and answer.is_correct)
        point_3_points = sum(1 for answer in student_answers if answer.question.point == 3 and answer.is_correct)


        account_group = AccountGroup.objects.filter(student=self.request.user, is_active=True).first()
        topics = account_group.group.course_topic.all()

        # Create or update StudentResult
        student_result, created = StudentResult.objects.get_or_create(student=self.request.user, status=True)
        student_result.point_1 = point_1_points
        student_result.point_2 = point_2_points * 2
        student_result.point_3 = point_3_points * 3
        student_result.exam_topics.set(topics)
        student_result.save()

        student = Account.objects.get(id=self.request.user.pk)
        student.status = False
        student.save()

        return redirect('exam_result')


class ExamResultView(AuthUserStatusMixin, ListView):
    model = StudentResult
    template_name = 'quiz-result.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["result"] = StudentResult.objects.filter(student=self.request.user, status=True).annotate(
            percent_point = F('total_point') * 5
        ).first()
        return context


def warning(request):
    return render(request, 'warning.html')
