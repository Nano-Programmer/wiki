from logging import PlaceHolder
import re
from random import randint, random
from . import views
from django.forms.fields import CharField
from django.forms.widgets import TextInput, Textarea
from django.urls.conf import path
from markdown2 import Markdown
from django.shortcuts import render
from . import util
from . import urls
from django.urls import reverse
from django.forms import forms
from django.http import HttpResponseRedirect
markdown = Markdown()

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        })

def title(request, entry):
    entries_list = util.list_entries()
    if entry in entries_list:
        file_content = util.get_entry(entry)
        title = entry
        return render(request, "encyclopedia/title.html", {
            "file_content" : markdown.convert(file_content),
            "title" : title
            })
    else:
        return render(request, "encyclopedia/entry_error.html")      
def search(request):
    results = []
    if request.method == "POST": 
        for i in util.list_entries():
            if i.lower() == request.POST["q"].lower():
                return HttpResponseRedirect(reverse("entry", kwargs={"entry" : i}))
            elif request.POST["q"].lower() in i.lower():
                results.append(i)
    return render(request, "encyclopedia/search.html",{
        "results" : results
    }) 
def create_entry(request):
    if request.method == "GET":
        return render(request, "encyclopedia/new_entry.html",)
    elif request.method == "POST":
        title = request.POST["title"]
        entry_list = util.list_entries()
        for i in entry_list:
            if i.lower() == request.POST["title"].lower():
                print("found")
                return render(request, "encyclopedia/new_entry_error.html")
        content = request.POST["content"]
        util.save_entry(title, content)
        return HttpResponseRedirect(reverse("entry", kwargs={"entry" : title}))           

def edit(request, entry):
    print(entry)
    if request.method == "GET":
        title = entry
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit.html",{
            "title" : title,
            "content" : content
        })
    elif request.method == "POST":
        title = request.POST["title"]
        content = request.POST["content"]
        util.save_entry(title, content)
        return HttpResponseRedirect(reverse("entry", kwargs={"entry" : title}))

def random(request):
    entry_list = util.list_entries()
    random_entry_no = randint(0, len(entry_list))
    title = entry_list[random_entry_no]
    return HttpResponseRedirect(reverse("entry", kwargs={"entry" : title}))
