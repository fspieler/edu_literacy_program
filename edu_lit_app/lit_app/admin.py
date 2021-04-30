from django.contrib import admin
from .models import Student, Test, Question, TestSubmission, Answer

admin.site.register(Student)
admin.site.register(Test)
admin.site.register(Question)
admin.site.register(TestSubmission)
admin.site.register(Answer)
