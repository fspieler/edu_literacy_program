from django.http import HttpResponse
from django.shortcuts import render
from lit_app.models import * 

def todo(request):
    data = {
        "tests": Test.objects.all()
    }
    return render(request, "todo.html", data)


def test_result(request):
    logger.warning(request)

