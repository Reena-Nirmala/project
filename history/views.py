from django.http import HttpResponse
from django.shortcuts import render
from text.models import TextSummary


def history(request):
    history = TextSummary.objects.filter(user1=request.session.get('user_id'))
    # print(history[0].input_text)
    # return HttpResponse("<h1>dfgergv</h1>")
    if history:
        return render(request, 'history.html', {'history': history})
    else:
        return render(request,'empty.html')
    # return TextSummary(history[0].input_text)