from django.shortcuts import render
from django.http import Http404, HttpResponse

# Create your views here.
def index(request):
    return render(request, "singlepage1/index.html")

texts = ["Lorem ipsum dolor sit amet consectetur adipisicing elit. Impedit, ipsum! Distinctio odit molestias culpa animi, ipsa incidunt fugiat unde sint, vitae quis odio itaque nulla ducimus dolore? Fugit, impedit aliquam!",
         "Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.",
         "Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."]

def section(request, num):
    if 1 <= num <= 3:
        return HttpResponse(texts[num - 1])
    else:
        return Http404
