from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

# database returns example list
contents = [
    {
        'author': 'nknk',
        'title':'my first post',
        'content': "This is my very first blogpost!",
        'date_posted': 'July 28, 2023'
    },
    {
        'author': 'khkh',
        'title':'my second post',
        'content': "This is my second blogpost!",
        'date_posted': 'July 27, 2023'
    }
]

@login_required
def home(request):
    # return HttpResponse('<h1>Welcome to the Dashboard!</h1>')
    context = {
        'contents': contents
    }
    # pass the data and access within the template
    return render(request, 'dashboard/index.html', context)
