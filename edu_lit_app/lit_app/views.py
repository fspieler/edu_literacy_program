import json
from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import redirect, render

from lit_app.models import * 
from lit_app.forms import * 

def todo(request):
    data = {
        "tests": Test.objects.all()
    }
    
    return render(request, "todo.html", data)


def start(request, test_id):
    student = Student.objects.first()
    test_submission = TestSubmission(
        test_id=test_id,
        student_id=student.id,
        start_time=datetime.now(),
        end_time=datetime.now()
    )
    test_submission.save()

    # Difficulty level starts with 1 
    difficulty = 1

    return redirect(f'/test/{test_submission.id}/next-question/{difficulty}')

    # return next_question(request, test_submission.id)

def next_question(request, test_submission_id, difficulty):

    student = Student.objects.first()

    test = TestSubmission.objects.get(id=test_submission_id).test
    
    # fetch all question with the current test id
    questions = Question.objects.filter(test_id=test.id).order_by('difficulty')

    # TODO: oick correct question
    current_question = questions[0]

    answer = Answer(
        test_id=test.id,
        test_submission_id=test_submission_id,
        start_time=datetime.now(),
        end_time=datetime.now(),
        student_id=student.id,
        question_id = current_question.id,
        content=''
    )
    answer.save()

    #first one without answer -- answers and then 
    # form = QuestionForm(instance=questions[0])

    return render(
        request,
        "question.html",
        {'test_submission_id': test_submission_id,
        'answer_id': answer.id,
        'question': current_question,
        'prompt': json.loads(current_question.answer_blob.replace("'", '"'))['prompt'],
        'answer_choices': json.loads(current_question.answer_blob.replace("'", '"'))['answers']
        })

