from django.shortcuts import redirect, render
from django.views.generic import ListView
from Account.models import StudentResult
from .models import Group, RandomQuestion
from django.views import View
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone



class AuthStaffSuperuserMixin:
    def dispatch(self, request, *args, **kwargs):
        # Check if the user is authenticated
        if request.user.is_authenticated:
            # Check if the user is staff or superuser
            if request.user.is_staff or request.user.is_superuser:
                return super().dispatch(request, *args, **kwargs)
            else:
                # User is authenticated but not staff or superuser, redirect to 404 page
                return render(request, '404.html')
        else:
            # User is not authenticated, redirect to login page or any other page as needed
            return redirect('login')  # Change 'login' to the actual login page URL



class SaveExamView(View):
    def post(self, request, *args, **kwargs):
        # Assuming the form data is submitted with the group ID (groupId)
        group_id = request.POST.get('groupId')

        if group_id:
            group = get_object_or_404(Group, pk=group_id)

            # Extract and update exam_durations
            exam_durations = request.POST.get('examDuration')
            if exam_durations:
                group.exam_durations = int(exam_durations)

            # Extract and update course_topics
            course_topics = request.POST.getlist('states[]')
            group.course_topic.set(course_topics)

            # Check if the checkbox is checked
            start_end_checkbox = request.POST.get('startEnd')
            if start_end_checkbox == 'on':
                group.is_checked=True

                tt = RandomQuestion.objects.filter(student__student_group__group=group).all()
                for t in tt:
                    t.status=False
                    t.save()
                
                ww = StudentResult.objects.filter(student__student_group__group=group).all()
                for w in ww:
                    if w.created_at.day != timezone.now().day:
                        w.status=False
                        w.save()

                # Set the status of all students in the group to True
                for account_group in group.account_group.filter(is_active=True):
                    account_group.student.status = True
                    account_group.student.save()
            else:
                group.is_checked=False

                # Set the status of all students in the group to False
                for account_group in group.account_group.filter(is_active=True):
                    account_group.student.status = False
                    account_group.student.save()

            # Save the updated group
            group.save()

            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Group ID not provided'})


class ExamStart(AuthStaffSuperuserMixin, ListView):
    model = Group
    template_name = 'dshb-forums.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["groups"] = Group.objects.filter(is_active=True).all()
        return context


def handler_not_found(request, exception):
    return render(request, '404.html')
