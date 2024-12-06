from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.forms import modelformset_factory
from decouple import config

from .models import (
    Student,
    Teacher,
    Classroom,
    Content,
    Difficulty,
)
from .forms import (
    StudentForm,
    TeacherForm,
    ClassroomForm,
    ContentForm,
    DifficultyForm,
)

import google.generativeai as genai

# Configuração do modelo de IA
genai.configure(api_key=config('API_KEY'))
model = genai.GenerativeModel("gemini-1.5-flash")


# Views relacionadas a estudantes
def list_students(request):
    students = Student.objects.all()
    return render(request, 'list_students.html', {'students': students})


def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_students')
    else:
        form = StudentForm()
    return render(request, 'add_student.html', {'form': form})


# Views relacionadas a professores
def list_teachers(request):
    teachers = Teacher.objects.all()
    return render(request, 'list_teachers.html', {'teachers': teachers})


def add_teacher(request):
    if request.method == 'POST':
        form = TeacherForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_teachers')
    else:
        form = TeacherForm()
    return render(request, 'add_teacher.html', {'form': form})


# Views relacionadas a turmas
def list_classrooms(request):
    classrooms = Classroom.objects.all()
    return render(request, 'list_classrooms.html', {'classrooms': classrooms})


def add_classroom(request):
    if request.method == 'POST':
        form = ClassroomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_classrooms')
    else:
        form = ClassroomForm()
    return render(request, 'add_classroom.html', {'form': form})


# Views relacionadas a conteúdos
def list_content(request):
    contents = Content.objects.all()
    return render(request, 'list_content.html', {'contents': contents})


def add_content(request):
    if request.method == 'POST':
        form = ContentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_classrooms')
    else:
        form = ContentForm()
    return render(request, 'add_content.html', {'form': form})


def edit_content(request, content_id):
    content = get_object_or_404(Content, id=content_id)
    if request.method == 'POST':
        form = ContentForm(request.POST, instance=content)
        if form.is_valid():
            form.save()
            return redirect('list_content')
    else:
        form = ContentForm(instance=content)
    return render(request, 'edit_content.html', {'form': form, 'content': content})


# Views relacionadas a dificuldades
def add_difficulty(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if request.method == 'POST':
        form = DifficultyForm(request.POST)
        if form.is_valid():
            form.save(student=student)
            return redirect('list_students')
    else:
        form = DifficultyForm()
    return render(request, 'add_difficulty.html', {'form': form, 'student': student})


def edit_difficulty(request, difficulty_id):
    difficulty = get_object_or_404(Difficulty, id=difficulty_id)
    if request.method == 'POST':
        form = DifficultyForm(request.POST, instance=difficulty)
        if form.is_valid():
            form.save()
            return redirect('list_students')
    else:
        form = DifficultyForm(instance=difficulty)
    return render(request, 'edit_difficulty.html', {'form': form, 'difficulty': difficulty})


# View principal
def home_view(request):
    return redirect('list_students')


# View para geração de relatórios com IA
def generate_report_view(request, id):
    try:
        student = get_object_or_404(Student, id=id)
        difficulties = Difficulty.objects.filter(student=student)

        prompt = f"""
        Relatório personalizado de atenção para o aluno {student.name}:

        1. **Informações sobre o aluno**:
        - Nome do Aluno: {student.name}
        - Idade: {student.age}

        2. **Dificuldades Identificadas**:
        - O aluno enfrenta dificuldades nas seguintes disciplinas:
        """

        for difficulty in difficulties:
            prompt += f"- **{difficulty.content.title}**: Nível de dificuldade {difficulty.get_level_display()} ({difficulty.feedback})\n"

        prompt += """
        3. **Atividades Sugeridas**:
        Sugira missões, desafios e atividades interativas para o aluno superar as dificuldades.
        """

        response = model.generate_content(prompt)
        ai_report = response.text

        return render(request, "report.html", {
            "student": student,
            "report": ai_report,
            "difficulties": difficulties,
        })

    except Exception as e:
        return HttpResponse(f"Erro: {str(e)}", status=500)
