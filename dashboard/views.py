from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

# database returns example list
contents = [

]

@login_required
def home(request):
    # return HttpResponse('<h1>Welcome to the Dashboard!</h1>')
    context = {
        'contents': contents
    }
    # pass the data and access within the template
    return render(request, 'dashboard/index.html', context)
