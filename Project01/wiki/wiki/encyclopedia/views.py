from django.shortcuts import render
import markdown
from random import randint

from . import util

def convert_md_to_html(title):
    content = util.get_entry(title)
    markdowner = markdown.Markdown()
    if content == None:
        return None
    else:
        return markdowner.convert(content)


def index(request):
    return render(request, "encyclopedia/index.html", {
    "entries": util.list_entries()
    })

def editPage(request):
    if request.method == "POST":
        title = request.POST['title']
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "content": content
        })
    
def savePage(request):
    if request.method == "POST":
        title = request.POST['title']
        content = request.POST['content']
        util.save_entry(title, content)
        html = convert_md_to_html(title)
        return render(request, "encyclopedia/entry.html",{
            "title": title,
            "content": html
        })

def newPage(request):
    if request.method == "GET":
        return render(request, "encyclopedia/new.html")
    else:
        title = request.POST['title']
        content = request.POST['content']

        #check if title exists
        titleExists = util.get_entry(title)
        if titleExists is not None:
            return render(request, "encyclopedia/error.html", {
                "error_message": "This entry already exists"
            })
        #add new entry
        else:
            util.save_entry(title, content)
            html = convert_md_to_html(title)
            return render(request, "encyclopedia/index.html", {
                "entries": util.list_entries()
            })

def random(request):
    num = randint(0, len(util.list_entries())-1)
    choice = util.list_entries()
    choice = choice[num]
    html = convert_md_to_html(choice)

    return render(request, "encyclopedia/entry.html",{
                "title": choice,
                "content": html
            })


def entry(request, title):
    html_content = convert_md_to_html(title)
    if html_content == None:
        return render(request, "encyclopedia/error.html", {
            "error_message": "This entry does not exist"
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": html_content,
        })

def search(request):
    if request.method == "POST":
        user_search = request.POST['q']
        html = convert_md_to_html(entry_search)

        if html is not None:
            return render(request, "encyclopedia/entry.html",{
                "title": user_search,
                "content": html
            })
        else:
            all_current_entries = util.list_entries()
            recommendations = []

            for entry in all_current_entries:
                if user_search.lower() in entry.lower():
                    recommendations.append(entry)
            return render(request, "encyclopedia/search.html",{
                "recommendations": recommendations
            })
        

    