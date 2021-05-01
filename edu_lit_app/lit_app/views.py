import json
import logging

from datetime import datetime
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import redirect, render

from lit_app.models import * 

logger = logging.getLogger(__name__)

ANSWERS_PER_TEST=5

def current_student():
    return Student.objects.first

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
        'prompt': json.loads(current_question.content.replace("'", '"'))['prompt'],
        'answer_choices': enumerate(json.loads(current_question.content.replace("'", '"'))['answers'])
        })

def answer(request, test_submission_id, answer_id):
    try:
        submission_record = TestSubmission.objects.filter(id=test_submission_id)[0]
        answer_record = Answer.objects.filter(id=answer_id)[0]
        question = answer_record.question
    except Exception as e:
        return HttpResponseNotFound(str(e))
    if request.method == 'POST':
        answer_record.content = request.POST
        detected_answer = answer_record.content['answer'][0]
        correct_answer = json.loads(question.content.replace("'", '"'))['correct_idx']
        correct = correct_answer == int(detected_answer)
        current_level = question.difficulty
        if correct:
            next_level = current_level + 1
        else:
            next_level = current_level - 1
        next_level = max(1, next_level)
        next_level = min(6, next_level)
        answer_record.save()

        number_answers = Answer.objects.filter(
            test_submission=submission_record
        ).count()
        if number_answers < ANSWERS_PER_TEST:
            return redirect(
                f'/test/{test_submission_id}/next-question/{next_level}'
            )
        return redirect(f'/test/{test_submission_id}')
