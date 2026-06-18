# StudyBuddy AI

StudyBuddy AI is a Django-based study assistant that helps students understand complex study material faster. Students can upload a PDF and use AI to generate summaries, flashcards, quizzes, simple explanations, and chat-style answers grounded in their notes.

This project was built as an internship project with one strict rule: the stack must use free services only. The backend uses Django and MySQL, uploaded PDFs are processed in memory, and Gemini is used through the free Google AI Studio API tier.

## Features

### 5 Study Modes

1. **summary** - Get AI-generated bullet-point summaries of your PDFs
2. **Flashcards** - Auto-generate interactive flip cards for active recall learning
3. **Quiz** - Create multiple-choice quizzes with instant scoring and feedback
4. **Explain** - Get simple explanations of complex concepts from your notes
5. **AI Tutor** - Chat with your PDFs and ask questions in real-time

### User Features

- **Guest Mode** - Try all features instantly without signing up (results not saved)
- **Account Mode** - Sign up to save your study sessions, flashcards, and quiz scores
- **Study Dashboard** - Track your progress with stats and recent activity
- **7-Day Study Plan** - AI generates personalized study schedules based on your weak areas
- **PDF Export** - Download any study result as a PDF
- **Responsive Design** - Works perfectly on desktop and mobile

---

## Tech Stack

- Backend: Django
- Database: MySQL/SQLite3
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

##  Prerequisites

- Python 3.11 or higher
- pip (Python package manager)
- Git
- Google Gemini API key (free from https://ai.google.dev/)
- MySQL 8.0 (for local development only)

## Setup (local development server)

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

##  Live Deployment

### Access the Live App

**StudyBuddy is deployed on Render and accessible worldwide!**

🔗 **Live Website:** https://studybuddy-ai-xtkd.onrender.com/

### How to Use

1. **Guest Mode**: Click "Try Free" to use all features without signing up
2. **Create Account**: Click "Create free account" to save your sessions
3. **Upload PDF**: Drag-drop or select any PDF file
4. **Choose Mode**: Select from Summary, Flashcards, Quiz, Explain, or AI Tutor
5. **Generate**: Click the generate button and wait for AI results
6. **Download**: Export results as PDF with one click

---
## 📖 Study Modes Explained

### 1. Summary Mode 📖

Condense long PDFs into structured bullet-point summaries.

**How it works:**
- Upload your PDF
- AI extracts key concepts and main ideas
- Results displayed in clean, readable format
- Export as PDF for offline reading

**Perfect for:** Textbooks, research papers, lecture notes

### 2. Flashcards Mode 🃏

Auto-generate interactive flip cards for spaced repetition learning.

**How it works:**
- Upload your study material
- AI creates question-answer pairs
- Cards render in a grid with flip animations
- Click any card to reveal the answer
- Study at your own pace

**Perfect for:** Vocabulary, definitions, key concepts

### 3. Quiz Mode 🎓

Test your knowledge with AI-generated multiple-choice questions.

**How it works:**
- Upload your notes
- AI generates MCQ with 4 options each
- Select your answers and click "Submit"
- Instant scoring with correct/incorrect highlights
- See detailed results breakdown

**Perfect for:** Exam preparation, self-assessment, knowledge testing

### 4. Explain Mode 💡

Get simple, clear explanations of complex topics from your notes.

**How it works:**
- Upload your material
- AI breaks down difficult concepts
- Results use everyday language
- Perfect for understanding, not memorizing

**Perfect for:** Complex topics, difficult chapters, confusing concepts

### 5. AI Tutor Mode 🤖

Chat with your PDFs in real-time using natural language.

**How it works:**
- Upload your study material
- Type any question about the content
- AI responds with contextual answers
- Ask follow-up questions instantly
- No character limits

**Perfect for:** Quick clarifications, detailed explanations, follow-up questions

---

## 👤 Account Features

### Guest Mode (No Signup Required)

✅ Access all 5 study modes instantly
✅ Upload unlimited PDFs
✅ Generate unlimited study materials
❌ Results NOT saved
❌ No study history

**Use Case:** Quick studying, trying the app before signing up

### Account Mode (Free Signup)

✅ All guest features PLUS:
✅ Save all study sessions
✅ View study history
✅ Track statistics (summaries, quizzes, flashcards created)
✅ Generate personalized 7-day study plans
✅ Build learning streaks
✅ Export results anytime

**Use Case:** Long-term learning, tracking progress, serious studying

### How to Create Account

1. Click **"Create free account"** on home page
2. Enter email and strong password
3. Click "Create Account"
4. Login with your credentials
5. All your sessions will be saved automatically

---

##  Dashboard & Analytics

Once logged in, your dashboard shows:

- **Streak Tracker**: Days studied consecutively
- **Study Statistics**: Total sessions, summaries, quizzes, flashcards created
- **Recent Activity**: Your 5 most recent study sessions
- **Quick Access**: Links to all study modes
- **7-Day Plan**: Personalized study schedule generated by AI

---

##  Security & Privacy

- `.env` file with sensitive keys is **NOT** uploaded to GitHub
- API keys stored securely on Render servers
- User passwords hashed using Django's default PBKDF2
- SQLite database stored locally (Render) with no external access
- All data stays encrypted in transit and at rest

---

## 📱 Responsive Design

StudyBuddy works on all devices:

- ✅ Desktop (Chrome, Firefox, Safari, Edge)
- ✅ Tablet (iPad, Android tablets)
- ✅ Mobile (iPhone, Android phones)

---

##  Troubleshooting

### "ModuleNotFoundError" Error

**Solution:** Reinstall dependencies
```bash
pip install -r requirements.txt
```

### "No such table" Error

**Solution:** Run migrations
```bash
python manage.py migrate
```

### GEMINI_API_KEY Not Set

**Solution:** Check your `.env` file has the correct key
```bash
# Verify the key is set
echo %GEMINI_API_KEY%
```

### Render Deployment Failed

**Solution:** Check Render logs for specific error:
1. Go to Render dashboard
2. Click your service
3. Check "Logs" tab for error messages


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
