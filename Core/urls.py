from django.urls import path
from .views import ExamStart, ProfileView, SaveExamView



urlpatterns = [
    path('exam_start/', ExamStart.as_view(), name='exam_start'),
    path('save_exam/', SaveExamView.as_view(), name='save_exam'),

    path('profile/', ProfileView.as_view(), name='profile'),
]

handler404 = "Core.views.handler_not_found"
