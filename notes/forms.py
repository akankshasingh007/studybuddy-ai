from django import forms
from .models import Note


class NoteForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super().clean()
        content = cleaned_data.get("content", "").strip()
        file = cleaned_data.get("file")

        if not content and not file:
            raise forms.ValidationError("Add written notes or upload a file before saving.")

        if file:
            allowed = (".pdf", ".txt", ".md")
            if not file.name.lower().endswith(allowed):
                raise forms.ValidationError("Upload a PDF, TXT, or Markdown file.")

        return cleaned_data

    class Meta:
        model = Note

        fields = [
            "title",
            "content",
            "file"
        ]

        widgets = {
            "content": forms.Textarea(
                attrs={
                    "rows": 10,
                    "placeholder": "Paste or type your study notes here..."
                }
            )
        }
