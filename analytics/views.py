from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def home(request):
    # user_goals = Goal.objects.filter(user=request.user)
    context = {
        'charts': 'charts',
    }

    return render(request, 'analytics/index.html', context)
