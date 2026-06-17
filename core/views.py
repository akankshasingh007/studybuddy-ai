from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from history.models import ChatSession
from notes.models import Note
from ai.gemini import run_gemini


def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'core/home.html')  # show landing, not redirect

def _activity_days(user):
    today = timezone.localdate()
    start = today - timedelta(days=29)
    days = set()

    for created_at in ChatSession.objects.filter(user=user, created_at__date__gte=start).values_list('created_at', flat=True):
        days.add(timezone.localtime(created_at).date())
    for created_at in Note.objects.filter(user=user, created_at__date__gte=start).values_list('created_at', flat=True):
        days.add(timezone.localtime(created_at).date())

    return today, days


def _current_streak(today, days):
    streak = 0
    check = today
    while check in days:
        streak += 1
        check -= timedelta(days=1)
    return streak


def _longest_streak(days):
    if not days:
        return 0
    longest = current = 0
    previous = None
    for day in sorted(days):
        if previous and (day - previous).days == 1:
            current += 1
        else:
            current = 1
        longest = max(longest, current)
        previous = day
    return longest


@login_required
def dashboard(request):
    sessions = request.user.sessions.all()
    today, active_days = _activity_days(request.user)

    stats = {
        'total': sessions.count(),
        'summaries': sessions.filter(mode='summary').count(),
        'quizzes': sessions.filter(mode='quiz').count(),
        'flashcards': sessions.filter(mode='flashcards').count(),
        'chats': sessions.filter(mode='chat').count(),
        'recent': sessions[:5],
        'streak': _current_streak(today, active_days),
        'longest_streak': _longest_streak(active_days),
        'active_days': len(active_days),
        'active_percent': min(100, round((len(active_days) / 30) * 100)),
        'notes_count': Note.objects.filter(user=request.user).count(),
        'uploaded_notes': Note.objects.filter(user=request.user).exclude(file='').exclude(file=None).count(),
        'written_notes': (Note.objects.filter(user=request.user, file='') | Note.objects.filter(user=request.user, file=None)).count(),
        'recent_notes': Note.objects.filter(user=request.user).order_by('-updated_at')[:5],
    }
    return render(request, 'core/dashboard.html', {'stats': stats})


@login_required
def study_plan(request):
    plan = None
    error = None

    if request.method == 'POST':
        sessions = request.user.sessions.all()[:20]
        notes = Note.objects.filter(user=request.user).order_by('-updated_at')[:10]
        if not sessions and not notes:
            error = 'Add a note or complete one study session before generating a plan.'
        else:
            history_context = '\n'.join([f"- {s.mode}: {s.title}" for s in sessions]) or 'No AI sessions yet.'
            notes_context = '\n'.join([f"- {n.title}: {n.preview}" for n in notes]) or 'No saved notes yet.'
            prompt_text = f"""Based on the following student's recent study sessions, create a personalized 7-day study plan.
Format each day as:
DAY 1: [Day name]
[Study tasks and topics for that day]

Recent sessions:
{history_context}

Saved notes:
{notes_context}

Make it specific, actionable, and encouraging."""
            plan = run_gemini('explain', prompt_text)
            import markdown as md
            if plan and not plan.startswith('Gemini error'):
                plan = md.markdown(plan)

    return render(request, 'core/study_plan.html', {'plan': plan, 'error': error})
