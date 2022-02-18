from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.utils import timezone
from .models import Question, Answer


def index(request):
    question_list = Question.objects.order_by('-create_date')
    context = { 'question_list': question_list }
    return render(request, 'community/question_list.html', context)


def detail(request, question_id):
    """
    detail 내용 출력
    """
    question = Question.objects.get(id=question_id)
    context = {'question': question}
    return render(request, 'community/question_detail.html', context)


def answer_create(request, question_id):

    question = get_object_or_404(Question, pk=question_id)
    answer = Answer(question=question, content=request.POST.get('content'), create_date=timezone.now())
    answer.save()
    return redirect('pybo:detail', question_id=question.id)


class IndexView(generic.ListView):
    """
    pybo 목록 출력
    """
    def get_queryset(self):
        return Question.objects.order_by('-create_date')


class DetailView(generic.DetailView):
    """
    pybo 내용 출력
    """
    model = Question