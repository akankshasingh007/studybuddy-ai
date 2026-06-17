# StudyBuddy AI

StudyBuddy AI is a Django-based study assistant that helps students understand complex study material faster. Students can upload a PDF and use AI to generate summaries, flashcards, quizzes, simple explanations, and chat-style answers grounded in their notes.

This project was built as an internship project with one strict rule: the stack must use free services only. The backend uses Django and MySQL, uploaded PDFs are processed in memory, and Gemini is used through the free Google AI Studio API tier.

## Features

- PDF upload with in-memory text extraction using `pdfplumber`
- Summary generation for long notes
- Flashcard generation for active recall
- Multiple-choice quiz generation with interactive scoring
- Simple explanation mode for difficult concepts
- Chat with uploaded notes using an AI tutor interface
- Guest mode with no saved data
- Authenticated mode with MySQL-backed history
- Markdown-rendered AI output
- Loading spinner for generation modes
- Animated typing bubbles in chat mode
- PDF export using `xhtml2pdf`
- Responsive sidebar-based student dashboard

## Tech Stack

- Backend: Django
- Database: MySQL
- AI: Gemini API with `google-genai`
- MySQL driver: `mysqlclient` with `PyMySQL` fallback
- PDF extraction: `pdfplumber`
- Markdown rendering: `Markdown`
- PDF export: `xhtml2pdf`
- Frontend: HTML, CSS, Bootstrap-style components

## Project Structure

```text
studybuddy/
├── ai/              # AI tool views, Gemini prompts, PDF extraction
├── core/            # Landing page and dashboard
├── history/         # Saved authenticated user history
├── notes/           # Notes app placeholder
├── static/          # CSS and frontend assets
├── templates/       # Django templates
├── users/           # Register, login, logout
├── studybuddy/      # Project settings and URLs
├── manage.py
└── requirements.txt
```

## Setup

1. Create and activate a virtual environment.

```bash
python -m venv venv
venv\Scripts\activate
```

2. Install dependencies.

```bash
pip install -r requirements.txt
```

3. Create a MySQL database, for example:

```sql
CREATE DATABASE studybuddy_db;
```

4. Copy `.env.example` to `.env` and fill in your values.

```env
SECRET_KEY=your-django-secret-key
DEBUG=True
DB_NAME=studybuddy_db
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_HOST=localhost
DB_PORT=3306
GEMINI_API_KEY=your_google_ai_studio_api_key
GEMINI_MODEL=gemini-2.5-flash
GEMINI_FALLBACK_MODEL=gemini-2.0-flash-lite
```

5. Run migrations.

```bash
python manage.py migrate
```

6. Start the development server.

```bash
python manage.py runserver
```

Open `http://127.0.0.1:8000/`.

## Free-Service Constraint

The project avoids paid cloud services and billing. It uses local Django/MySQL development plus the free Gemini API tier from Google AI Studio. If the daily quota is exhausted during testing, switch the model in `.env` to a lighter free-tier model such as:

```env
GEMINI_MODEL=gemini-2.0-flash-lite
```

## Data Handling

- Uploaded PDFs are processed in memory and are not saved to disk.
- Guest mode stores extracted text only temporarily in the session.
- Authenticated mode saves generated interactions to MySQL history.
- API keys and database passwords belong in `.env`, which is ignored by git.

## Development Phases Covered

1. Django project setup
2. MySQL configuration
3. User authentication
4. Guest mode
5. PDF upload
6. In-memory PDF extraction
7. Gemini API integration
8. Summary generation
9. Flashcard generation
10. Quiz generation
11. Explain mode
12. Chat-with-notes mode
13. UI polish, history, and export

## Notes

- Use `google-genai`, not the deprecated `google-generativeai` package.
- On Windows, `xhtml2pdf` is used for PDF export because it is easier to run than WeasyPrint.
- MySQL may not be available in PATH on Windows; MySQL Workbench can still be used to create and inspect the database.
- If `mysqlclient` fails to install on Windows, the included `PyMySQL` fallback can still connect Django to MySQL.
