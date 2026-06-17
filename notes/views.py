from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Note
from .forms import NoteForm
from ai.pdf_utils import extract_text_from_study_file


@login_required
def notes_list(request):
    notes = Note.objects.filter(user=request.user).order_by('-created_at')
    uploaded_notes = notes.exclude(file='').exclude(file=None)
    created_notes = notes.filter(file='') | notes.filter(file=None)
    created_notes = created_notes.order_by('-created_at')
    return render(request, 'notes/list.html', {
        'uploaded_notes': uploaded_notes,
        'created_notes': created_notes,
    })


@login_required
def create_note(request):
    if request.method == 'POST':
        form = NoteForm(request.POST, request.FILES)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            if note.file:
                text, err = extract_text_from_study_file(note.file)
                if text:
                    note.content = f"{note.content}\n\n{text}".strip()
                elif err:
                    messages.warning(request, err)
                note.file.seek(0)
            note.save()
            messages.success(request, f'"{note.title}" saved successfully.')
            return redirect('notes')
    else:
        form = NoteForm()
    return render(request, 'notes/create.html', {'form': form})


@login_required
def delete_note(request, pk):
    note = get_object_or_404(Note, id=pk, user=request.user)
    note.delete()
    messages.success(request, 'Note deleted.')
    return redirect('notes')


@login_required
def use_note(request, pk):
    """Load a saved note's content into session and redirect to AI tool."""
    note = get_object_or_404(Note, id=pk, user=request.user)
    mode = request.GET.get('mode', 'summary')
    if mode == 'tutor':
        mode = 'chat'

    # Get text content
    text = note.content
    if not text and note.file:
        text, err = extract_text_from_study_file(note.file)
        if text:
            note.content = text
            note.save()

    if text:
        request.session['extracted_text'] = text[:12000]
        request.session['pdf_name'] = note.title
        request.session.modified = True
        return redirect(f'/ai/?mode={mode}')
    else:
        messages.error(request, 'Could not extract text from this note.')
        return redirect('notes')
