from django.shortcuts import render

from django import forms

import markdown

from . import util

from django.urls import reverse
from django.http import HttpResponseRedirect

import random


def convert_to_html(title):
    # ene hesgiig anhaarch avah
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
    

def entry(request, title):
    html_content = convert_to_html(title)
    if html_content == None:
        return render(request, "encyclopedia/error.html",{
            "message":"This entry doesn't exit."
        })
    else:
        return render(request, "encyclopedia/entry.html",{
            "title":title,
            "content":html_content
        })

def search(request):
    if request.method == "POST":
        entry_search = request.POST['q']
        html_content = convert_to_html(entry_search)
        if html_content is not None:
            return render(request, "encyclopedia/entry.html",{
            "content":html_content
        })
        else:
            # Ene hesgiig anhaarch avah
            lists = util.list_entries()
            arr = []
            for list in lists:
                if entry_search.lower() in list.lower():
                    arr.append(list)
            if len(arr)>0:
                return render(request, "encyclopedia/search.html",{
                    "arr":arr
                })
            else:
                return render(request, "encyclopedia/error.html",{
                    "message":"Not found!"
                })

def create(request):
    if request.method == "GET":
        return render(request, "encyclopedia/create.html")
    else:
        title = request.POST['title']
        content = request.POST['content']
        exist = convert_to_html(title)
        if exist is not None:
            return render(request, "encyclopedia/error.html",{
                "message":"Already exist!"
            })
        else:
            util.save_entry(title, content)
            return render(request, "encyclopedia/entry.html",{
                "title":title,
                "content":content
            })

def edit(request):
    if request.method == "GET":
        title = request.GET['entry_title']
        content = convert_to_html(title)
        return  render(request, "encyclopedia/edit.html",{
            "value1":title,
            "value2":content
        })
    else:
        title = request.POST['title']
        content = request.POST['content']
        util.save_entry(title, content)
        return render(request, "encyclopedia/entry.html",{
            "title" : title,
            "content":content
        })

def random1(request):
    title = util.list_entries()
    rand_title = random.choice(title)
    html_content = convert_to_html(rand_title)
    return render(request, "encyclopedia/entry.html",{
        "title":rand_title,
        "content":html_content
    })