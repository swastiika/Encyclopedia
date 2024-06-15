from django.shortcuts import render
from . import util
def index(request):
    return render(request,"encyclopedia/index.html", {
        "entries": util.list_entries()
    })
def entry(request,name):
    entity = util.convert_md_to_html(name)
    if entity==None:
        return render(request,"encyclopedia/error.html",{"message":"this entry does not exist"})
    else:
        return render(request,"encyclopedia/entry.html",{
            "title":name,
            "content": entity
        })
    
def search(request):
    if request.method=='POST':
        search_entry = request.POST['q']
        entity= util.convert_md_to_html(search_entry)
        if entity is not None:
            return render(request,"encyclopedia/entry.html",{
                "title":search_entry,
                "content":entity

            })
        else:
            allEntries = util.list_entries()
            recommendation=[]
            for entry in allEntries:
                if search_entry.lower() in entry.lower():
                    recommendation.append(entry)

            return render(request,"encyclopedia/search.html",{"recommendation":recommendation})    
        
def new_page(request):
    if request.method=="GET":
        return render(request,"encyclopedia/new.html")  

    else:
        title = request.POST['title'] 
        content = request.POST['content']
        titleExist = util.get_entry(title)
        if titleExist is not None:
            return render(request,"encyclopedia/error.html",{
                "message":"entry page already exists"
            })
        else:
            util.save_entry(title,content)
            html_content = util.convert_md_to_html(title)
            return render(request,"encyclopedia/entry.html",{
                "title": title,
                "content":html_content
            })
def edit(request):
    if request.method== 'POST':
        title= request.POST['entry_title']
        content = util.get_entry(title)
        return render(request,"encyclopedia/edit.html",{
            "title":title,
            "content":content
        })
    
def save_edit(request):
    if request.method =="POST":
        title= request.POST['title']
        content = request.POST['content']
        util.save_entry(title,content)
        html_content = util.convert_md_to_html(title)
        return render(request,"encyclopedia/entry.html"),{
            "title":title,
            "content":html_content
        }