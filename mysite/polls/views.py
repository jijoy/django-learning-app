from django.db.models import F
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.urls import reverse

from .models import Question,Choice


# Create your views here.

def index(request):
    question_list = Question.objects.order_by("-pub_date")[:5]
    context = {
        "question_list": question_list
    }
    return render(request,"polls/index.html",context)

def details(request,question_id):
    try:
        question = Question.objects.get(pk=question_id)
        context = {
            "question": question
        }
    except Question.DoesNotExist:
        raise Http404("Question doesn't exist")
    return render(request,"polls/details.html", context)

def results(request, question_id):
    question = get_object_or_404(Question,pk=question_id)
    return render(request,'polls/results.html', {"question":question})

def vote(request, question_id):
    question = get_object_or_404(Question,pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError,Choice.DoesNotExist):
        return render(
            request,"polls/details.html",
            {"question":question,"error_message":"You didn't select a choice"
             })
    else:
        selected_choice.votes=F("votes")+1
        selected_choice.save()
        return HttpResponseRedirect(reverse("polls:results",args=(question.id,)))