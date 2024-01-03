from django.shortcuts import render


def allresult(request):
    return render(request, 'dshb-participants.html')
