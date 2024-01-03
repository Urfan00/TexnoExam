from django.urls import path
from .views import ExamResultView, QuizView, RuleView, warning



urlpatterns = [
    path('', RuleView.as_view(), name='index'),
    path('quiz/', QuizView.as_view(), name='quiz'),
    path('exam_result/', ExamResultView.as_view(), name='exam_result'),
    path('warning/', warning, name='warning'),
]
