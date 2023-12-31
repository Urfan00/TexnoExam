from django.shortcuts import redirect
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetConfirmView, PasswordChangeView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import UserPassesTestMixin
from .forms import ChangePasswordForm, CustomSetPasswordForm, LoginForm, ResetPasswordForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout



def logout_view(request):
    logout(request)
    return redirect('login')


class LogInView(LoginView, UserPassesTestMixin):
    template_name = 'login.html'
    form_class = LoginForm

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('profile')
        return super().get(request, *args, **kwargs)

    def test_func(self):
        return not (self.request.user.is_superuser or self.request.user.is_staff)

    def get_success_url(self):
        if self.request.user.is_authenticated and self.test_func():
            if hasattr(self.request.user, 'first_time_login') and self.request.user.first_time_login:
                return reverse_lazy('change_password')
            else:
                return reverse_lazy('profile')
        elif self.request.user.is_authenticated:
            return reverse_lazy('exam_start')
        return reverse_lazy('profile')



class ChangePasswordView(LoginRequiredMixin, PasswordChangeView):
    template_name='change-password.html'
    form_class= ChangePasswordForm
    success_url = reverse_lazy('logout')

    def form_valid(self, form):
        # Call the parent class's form_valid method to perform the password change

        # Update the first_time_login attribute to False
        self.request.user.first_time_login = False
        self.request.user.save()

        return super().form_valid(form)



class ResetPasswordView(PasswordResetView):
    template_name = 'reset_pwd/forget-password.html'
    form_class = ResetPasswordForm
    email_template_name = 'reset_pwd/reset_password_email.html'
    subject_template_name = 'reset_pwd/reset_password_subject.txt'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      "If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."

    success_url = reverse_lazy('logout')


class ResetPasswordConfirmView(PasswordResetConfirmView):
    template_name='reset_pwd/reset_password_confirm.html'
    form_class=CustomSetPasswordForm
    success_url = reverse_lazy('logout')


