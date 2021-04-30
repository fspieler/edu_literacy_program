from django.db import models

class Student(models.Model):
    first_name = models.CharField(max_length=30,default=None)
    id = models.BigAutoField(primary_key=True)
    last_name = models.CharField(max_length=30, default=None)

class Test(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=30, default=None)

class Question(models.Model):
    name = models.CharField(max_length=30,default=None)
    id = models.BigAutoField(primary_key=True)
    difficulty = models.IntegerField()
    answer_blob = models.TextField()
    test = models.ForeignKey(Test, on_delete=models.CASCADE)

class TestSubmission(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=30, default=None)
    is_complete = models.BooleanField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    test = models.ForeignKey(Test, on_delete=models.CASCADE)

class Answer(models.Model):
    id = models.BigAutoField(primary_key=True)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    content = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    test_submission = models.ForeignKey(TestSubmission, on_delete=models.CASCADE)