from django.shortcuts import render
from django import forms


class NewTaskForm(forms.Form):
    task = forms.CharField(label="New Task")

# Create your views here.
tasks = ["foo", "bar", "baz"]

def index(request):
    return render(request, "tasks/index.html",{
        "tasks": tasks
    })

def add(request):
    return render(request, "tasks/add.html", {
        "form": NewTaskForm()
    })