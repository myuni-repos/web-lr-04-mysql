from django import forms
import datetime
from django.core.exceptions import NON_FIELD_ERRORS
from .models import Grade

class GradeForm(forms.Form):
    STORAGE_CHOICES = [
        ('file', 'Файл'),
        ('database', 'База данных'),
    ]
    FORMAT_CHOICES = [
        ('json', 'JSON'),
        ('xml', 'XML')
    ]

    student_name = forms.CharField(max_length=100, label="Имя студента")
    group = forms.CharField(max_length=20, label="Группа")
    subject = forms.CharField(max_length=100, label="Предмет")    
    grade = forms.IntegerField(min_value=1, max_value=5, label="Оценка")
    date = forms.DateField(
        initial=datetime.date.today,
        widget=forms.DateInput(attrs={'type': 'date'}),
        label="Дата сдачи"
    )
    teacher = forms.CharField(max_length=100, label="Преподаватель")    
    storage = forms.ChoiceField(choices=STORAGE_CHOICES, label="Куда сохранить")
    file_format = forms.ChoiceField(choices=FORMAT_CHOICES, label="Формат файла", required=False)

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('storage') == 'file' and not cleaned_data.get('file_format'):
            self.add_error('file_format', 'Выберите формат файла.')
        return cleaned_data


class GradeDatabaseForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ['student_name', 'group', 'subject', 'grade', 'date', 'teacher']
        widgets = {'date': forms.DateInput(attrs={'type': 'date'})}
        error_messages = {
            NON_FIELD_ERRORS: {'unique_together': 'Такая запись уже существует в базе данных.'},
        }

    def clean_grade(self):
        grade = self.cleaned_data['grade']
        if not 1 <= grade <= 5:
            raise forms.ValidationError('Оценка должна быть от 1 до 5.')
        return grade

    def clean(self):
        cleaned_data = super().clean()
        fields = ['student_name', 'group', 'subject', 'date', 'teacher']
        if all(cleaned_data.get(field) for field in fields):
            duplicates = Grade.objects.filter(**{field: cleaned_data[field] for field in fields})
            if self.instance.pk:
                duplicates = duplicates.exclude(pk=self.instance.pk)
            if duplicates.exists():
                raise forms.ValidationError('Такая запись уже существует в базе данных.')
        return cleaned_data


class UploadFileForm(forms.Form):
    file = forms.FileField(label="Выберите XML или JSON файл")
