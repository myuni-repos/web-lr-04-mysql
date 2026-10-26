from django.shortcuts import render
from django.db import IntegrityError
from .forms import GradeForm, UploadFileForm, GradeDatabaseForm
from .models import Grade
from .utils import save_grade_to_file, get_all_grades, process_uploaded_file

def index(request):
    message = ''
    
    if request.method == 'POST':
        form = GradeForm(request.POST)
        
        if form.is_valid():
            if form.cleaned_data['storage'] == 'file':
                save_grade_to_file(form.cleaned_data)
                message = 'Данные успешно сохранены в файл!'
                form = GradeForm()
            else:
                grade_form = GradeDatabaseForm(form.cleaned_data)
                if grade_form.is_valid():
                    try:
                        grade_form.save()
                        message = 'Данные успешно сохранены в базу данных!'
                        form = GradeForm()
                    except IntegrityError:
                        form.add_error(None, 'Такая запись уже существует в базе данных.')
                else:
                    for field, errors in grade_form.errors.items():
                        for error in errors:
                            form.add_error(None if field == '__all__' else field, error)
    else:
        form = GradeForm()
        
    context = {
        'form': form,
        'message': message
    }
    
    return render(request, 'grades/index.html', context)

def file_list(request):
    grades = get_all_grades()
    
    message = ''
    if not grades:
        message = 'На сервере пока нет ни одного файла с данными (или папка пуста).'
        
    context = {
        'grades': grades,
        'message': message
    }
    
    return render(request, 'grades/file_list.html', context)

def upload_file(request):
    message = ''
    is_error = False
    
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        
        if form.is_valid():
            file_obj = request.FILES['file']
            success, msg = process_uploaded_file(file_obj)
            
            message = msg
            is_error = not success
            if success:
                form = UploadFileForm()
    else:
        form = UploadFileForm()
        
    context = {
        'form': form,
        'message': message,
        'is_error': is_error
    }
    return render(request, 'grades/upload.html', context)
