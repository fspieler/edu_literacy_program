from django.urls import path
from . import views

urlpatterns = [
    path("todo/", views.todo, name = "todo"),
    path("test/<int:test_id>/start", views.start, name = "start"),
    path("test/<int:test_submission_id>/next-question", views.next_question, name = "next-question")
]