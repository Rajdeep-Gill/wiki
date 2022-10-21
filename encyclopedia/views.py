from django.shortcuts import render, redirect
from django import forms
from markdown2 import Markdown
from . import util
import random


class CreateForm(forms.Form):
    title = forms.CharField(label='', widget=forms.TextInput(
    attrs={
        "placeholder": "Page Title",
        'minlength': 1,
        'size': 50
    }))
    text = forms.CharField(label='', widget=forms.Textarea(
    attrs={
        "placeholder": "Enter Page Content using Github Markdown",
        'rows': 5,
        'cols': 5, 
        'size': 25
    }))

class EditForm(forms.Form):
    text = forms.CharField(label='', widget=forms.Textarea(
    attrs={
        "placeholder": "Enter Page Content using Github Markdown",
    }))
    


def index(request):
    return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries(),
            "title": "All Pages",
    })

def randomPage(request):
    randomPage = random.choice(util.list_entries())
    return redirect('entries', title=randomPage)


def entries(request, title):
    entryMD = util.get_entry(title)

    if entryMD != None:
        entryMD = Markdown().convert(entryMD)
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "entry": entryMD
        })
       
def search(request):
    searchQuery = request.GET.get('q')
    relatedTitles = util.related_entries(searchQuery)
    for title in relatedTitles:
        if searchQuery.lower() == title.lower():
            return render(request, "encyclopedia/entry.html", {
                "title": searchQuery,
                "entry": Markdown().convert(util.get_entry(searchQuery))
            })   
    if len(relatedTitles) > 0:
        return render(request, "encyclopedia/index.html", {
            "entries": relatedTitles,
            "title": "Related Pages for the search: " + searchQuery
        })
    else:
        return render(request, "encyclopedia/index.html", {
            "title": "No Pages Found for the search: " + searchQuery
            })

def newPage(request):
    #Display a blank form
    if request.method == 'POST':
        form = CreateForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            text = form.cleaned_data['text']
            
            #Check if the title already exists
            if util.get_entry(title) != None:
                return render(request, "encyclopedia/create.html", {
                    "form": form,
                    "error": "Page already exists"
                })
            #Save the new page
            else:
                util.save_entry(title, text)
                return render(request, "encyclopedia/entry.html", {
                    "title": title,
                    "entry": Markdown().convert(text)
                })

    return render(request, "encyclopedia/new_page.html", {
            'form' : CreateForm(),
    })

def edit(request, title):
    #Retrieve the entry and display it in the form
    if request.method == "GET":
        text = util.get_entry(title)

        return render(request, "encyclopedia/edit.html", {
          "title": title,
          "edit_form": EditForm(initial={'text':text}),
        })

    #Submit changes
    elif request.method == "POST":
        form = EditForm(request.POST)

        if form.is_valid():
          text = form.cleaned_data['text']
          util.save_entry(title, text)
          return entries(request, title)

      

            

    