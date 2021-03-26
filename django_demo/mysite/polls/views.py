from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.views import generic

from .models import Question, Choice


class IndexView(generic.ListView):
    """
    IndexView
    """
    template_name = "polls/index.html"
    content_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Return the last five published questions.
        @return:
        """
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    """
    DetailView
    """
    model = Question
    template_name = "polls/detail.html"

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        @return:
        """
        return Question.objects.filter(pub_date__year=timezone.now())


class ResultsView(generic.DetailView):
    """
    ResultsView
    """
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    """
    vote
    @param request:
    @param question_id:
    @return:
    """
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


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
    question = get_object_or_404(Question, pk=question_id)

    return render(request, 'polls/results.html', {'question': question})
