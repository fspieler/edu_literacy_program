from django.urls import path
from . import views

urlpatterns = [
    path("todo/", views.todo, name = "todo")
    path("test/<int:test_submission_id>", views.test_result, name="test result")
]
