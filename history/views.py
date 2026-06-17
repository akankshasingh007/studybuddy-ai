from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import ChatSession


@login_required
def history_list(request):
    sessions = request.user.sessions.all()
    return render(request, 'history/list.html', {'sessions': sessions})


@login_required
def session_detail(request, pk):
    session = get_object_or_404(ChatSession, pk=pk, user=request.user)
    return render(request, 'history/detail.html', {'session': session})