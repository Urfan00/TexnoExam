from django.urls import path
from .views import QuizView, RuleView



urlpatterns = [
    path('', RuleView.as_view(), name='index'),
    path('quiz/', QuizView.as_view(), name='quiz')
]
