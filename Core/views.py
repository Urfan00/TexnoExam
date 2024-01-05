from django.shortcuts import redirect, render
from django.views.generic import ListView
from .models import Group
from django.views import View
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import UserPassesTestMixin



class SuperuserRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        return render(self.request, '404.html')


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
            if course_topics:
                group.course_topic.set(course_topics)

            # Check if the checkbox is checked
            start_end_checkbox = request.POST.get('startEnd')
            if start_end_checkbox == 'on':
                group.is_checked=True

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


class ExamStart(SuperuserRequiredMixin, ListView):
    model = Group
    template_name = 'dshb-forums.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["groups"] = Group.objects.filter(is_active=True).all()
        return context
