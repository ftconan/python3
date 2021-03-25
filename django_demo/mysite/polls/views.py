from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404

from .models import Question


def index(request):
    """
    index
    @param request:
    @return:
    """
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {
        "latest_question_list": latest_question_list,
    }

    return render(request, "polls/index.html", context)


def detail(request, question_id):
    """
    detail
    @param request:
    @param question_id:
    @return:
    """
    # try:
    #     question = Question.objects.get(pk=question_id)
    # except Question.DoesNotExist:
    #     raise Http404("Question does not exist")

    question = get_object_or_404(Question, pk=question_id)

    return render(request, 'polls/detail.html', {'question': question})


def results(request, question_id):
    """
    results
    @param request:
    @param question_id:
    @return:
    """
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)


def vote(request, question_id):
    """
    vote
    @param request:
    @param question_id:
    @return:
    """
    return HttpResponse("You're voting on question %s." % question_id)
