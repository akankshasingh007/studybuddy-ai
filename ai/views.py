from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .pdf_utils import extract_text_from_study_file
from .gemini import run_gemini
from history.models import ChatSession, Message
from notes.models import Note
from django.http import HttpResponse
from xhtml2pdf import pisa
import io
import markdown

MODES = [
    'summary',
    'flashcards',
    'quiz',
    'explain',
    'chat',
    'revision'
]

def ai_tool(request):
    """Main AI tool view. Guests use session-only files; accounts can reuse saved notes."""
    if request.method == 'GET' and 'mode' not in request.GET:
        request.session.pop('extracted_text', None)
        request.session.pop('pdf_name', None)
        request.session.pop('last_result', None)
        request.session.pop('last_mode', None)
        request.session.modified = True

    result = None
    error = None
    mode = request.GET.get('mode', 'summary')
    extracted_text = request.session.get('extracted_text', '')

    if mode not in MODES:
        mode = 'summary'

    if request.method == 'POST':
        action = request.POST.get('action')
        mode = request.POST.get('mode', mode)

        if action == 'upload':
            study_file = request.FILES.get('pdf')
            save_to_notes = request.POST.get('save_to_notes') == 'on'
            if not study_file:
                error = "Please upload a PDF, TXT, or Markdown file."
            else:
                text, err = extract_text_from_study_file(study_file)
                if err:
                    error = err
                else:
                    request.session['extracted_text'] = text
                    request.session['pdf_name'] = study_file.name
                    request.session.modified = True
                    extracted_text = text
                    if request.user.is_authenticated and save_to_notes:
                        study_file.seek(0)
                        Note.objects.create(
                            user=request.user,
                            title=study_file.name,
                            file=study_file,
                            content=text,
                        )
                        messages.success(request, f'"{study_file.name}" loaded and saved to your notes.')
                    else:
                        messages.success(request, f'"{study_file.name}" loaded successfully.')

        elif action == 'write':
            title = request.POST.get('written_title', '').strip() or 'Untitled note'
            text = request.POST.get('written_content', '').strip()
            save_to_notes = request.POST.get('save_to_notes') == 'on'
            if not text:
                error = "Write or paste notes before loading them."
            else:
                request.session['extracted_text'] = text[:12000]
                request.session['pdf_name'] = title
                request.session.modified = True
                extracted_text = text[:12000]
                if request.user.is_authenticated and save_to_notes:
                    Note.objects.create(user=request.user, title=title, content=text)
                    messages.success(request, f'"{title}" loaded and saved to your notes.')
                else:
                    messages.success(request, f'"{title}" loaded for this session.')

        elif action == 'load_note':
            if not request.user.is_authenticated:
                error = "Sign in to use saved notes."
            else:
                note_id = request.POST.get('note_id')
                note = get_object_or_404(Note, id=note_id, user=request.user)
                text = note.content
                if not text and note.file:
                    text, err = extract_text_from_study_file(note.file)
                    if text:
                        note.content = text
                        note.save(update_fields=['content', 'updated_at'])
                if text:
                    request.session['extracted_text'] = text[:12000]
                    request.session['pdf_name'] = note.title
                    request.session['last_result'] = ''
                    request.session['last_mode'] = ''
                    request.session.modified = True
                    extracted_text = text[:12000]
                    messages.success(request, f'"{note.title}" loaded for {mode.title()}.')
                else:
                    error = "Could not extract text from this note."

    
        elif action == 'generate':
            mode = request.POST.get('mode', 'summary')
            question = request.POST.get('question', '')
            extracted_text = request.session.get('extracted_text', '')

            if not extracted_text:
                error = "Please upload a file or choose a saved note first."
            elif mode == 'chat' and not question.strip():
                error = "Please enter a question."
            else:
                result = run_gemini(mode, extracted_text, question)
                if result and not result.startswith('Gemini error'):
                    result = markdown.markdown(result, extensions=['extra', 'sane_lists'])
                request.session['last_result'] = result
                request.session['last_mode'] = mode
                request.session.modified = True

                
                if request.user.is_authenticated and result and not result.startswith('Gemini error'):
                    pdf_name = request.session.get('pdf_name', 'Untitled')
                    session = ChatSession.objects.create(
                        user=request.user,
                        title=f"{pdf_name} — {mode.title()}",
                        mode=mode,
                    )
                    Message.objects.create(
                        session=session,
                        user_input=extracted_text[:500] + '...',
                        ai_response=result,
                    )

        
        elif action == 'clear':
            request.session.pop('extracted_text', None)
            request.session.pop('pdf_name', None)
            request.session.pop('last_result', None)
            request.session.pop('last_mode', None)
            extracted_text = ''
            request.session.modified = True

    context = {
        'result': result,
        'error': error,
        'mode': mode,
        'pdf_loaded': bool(extracted_text),
        'pdf_name': request.session.get('pdf_name', ''),
        'modes': MODES,
        'saved_notes': Note.objects.filter(user=request.user).order_by('-updated_at')[:20] if request.user.is_authenticated else [],
    }
    return render(request, 'ai/tool.html', context)
def export_pdf(request):
    result = request.session.get('last_result', '')
    mode = request.session.get('last_mode', 'result')
    if not result:
        return redirect('ai_tool')

    html_content = f"""
    <html>
    <head>
    <style>
        body {{ font-family: Arial, sans-serif; padding: 2rem; color: #1a1a1a; }}
        h1 {{ color: #0ea5e9; border-bottom: 2px solid #0ea5e9; padding-bottom: 0.5rem; }}
        ul {{ line-height: 1.8; }}
        li {{ margin: 0.4rem 0; }}
    </style>
    </head>
    <body>
    <h1>StudyBuddy AI — {mode.title()}</h1>
    {result}
    </body>
    </html>
    """

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="studybuddy_{mode}.pdf"'
    pisa.CreatePDF(io.StringIO(html_content), dest=response)
    return response
