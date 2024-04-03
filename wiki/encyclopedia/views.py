from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from . import util
import random
import markdown2

def index(request):
    if request.method == "POST":
        title = request.POST.get("title")
        table = [x.upper() for x in util.list_entries()]
        if title.upper() in table:
            return render(request, "encyclopedia/exist.html",{"entry" : title})
        else:
            content = request.POST.get("content")
            util.save_entry(title,content)
            return HttpResponseRedirect(reverse("note:entry",kwargs={'title': title}))
        
    query = request.GET.get("q",default="")
    if query == "":
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries()
        })
    else:
        table = [x.upper() for x in util.list_entries()]
        if query.upper() in table:
            return HttpResponseRedirect(reverse("note:entry",kwargs={'title': query}))
        else:
            results = []
            table2 = util.list_entries()
            for i in range(len(table)):
                if query.upper() in table[i]:
                    results.append(table2[i])
            return render(request, "encyclopedia/result.html", {
            "results" : results, "empty" : results == []
            })
        

def entry(request, title):
    content = util.get_entry(title)
    if request.method == "POST":
        mod = request.POST.get("mod")
        if mod == "Edit":
           return render(request, "encyclopedia/edit.html",{"content":content,"title":title})
        elif mod == "Delete" :
            return render(request, "encyclopedia/delete.html",{"title":title})
    if content == None:
        return
    else:
        return render(request, "encyclopedia/content.html", {
        "title" : title, "content": markdown2.markdown(content)
    })

def create(request):
    return render(request,"encyclopedia/create.html")

def redirect_to_note(request):
    return HttpResponseRedirect(reverse("note:index"))

def edit(request):
    title = request.POST.get("title")
    content = request.POST.get("content")
    util.save_entry(title,content)
    return HttpResponseRedirect(reverse("note:entry",kwargs={'title': title}))

def delete(request):
    title = request.POST.get("title")
    sure = request.POST.get("sure")
    if sure == "true":
        util.delete_entry(title)
        return HttpResponseRedirect(reverse("note:index"))
    else:
        return HttpResponseRedirect(reverse("note:entry",kwargs={'title': title}))
    
def randompick(reuest):
    pick = random.choice(util.list_entries())
    return HttpResponseRedirect(reverse("note:entry",kwargs={'title': pick}))