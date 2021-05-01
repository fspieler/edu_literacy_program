import logging

from django.http import HttpResponse
from django.shortcuts import render
from lit_app.models import * 

logger = logging.getLogger(__name__)

def todo(request):
    data = {
        "tests": Test.objects.all()
    }
    return render(request, "todo.html", data)


def test_result(request, test_submission_id):
    logger.warning(request)
    logger.warning(test_submission_id)

    record = TestSubmission.objects.filter(pk=test_submission_id)
    data = {

    }




