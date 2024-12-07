from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.forms import modelformset_factory
from decouple import config
from django.utils.safestring import mark_safe

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


def edit_difficulty(request, id):
    difficulty = get_object_or_404(Difficulty, id=id)
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

def generate_report_view(request, id):
    try:
        # Obtém o aluno e suas dificuldades
        student = get_object_or_404(Student, id=id)
        difficulties = Difficulty.objects.filter(student=student)

        # Lista para armazenar relatórios das dificuldades
        ai_reports = []

        for difficulty in difficulties:
            # Construção do prompt
            prompt = f"""
            Baseado nas dificuldades do aluno {student.name}:
            Nível de dificuldade: {difficulty.get_level_display()}
            Conteúdo da dificuldade: {difficulty.content.title}\n
            Sobre a dificuldade: {difficulty.feedback}
            (Não é necessário reescrever os dados mencionados na resposta.)
            Crie um relatório detalhado sobre o aluno {student.name} usando HTML. O relatório deve incluir fórmulas em MathML, se necessário.
            Estruture o HTML como um componente <div> contendo:
            1. Atividades Sugeridas:
               - Sugira missões, desafios e atividades interativas personalizadas para superar as dificuldades.

            2. Exemplos de exercício:
               - exercícios básicos, baseados na dificuldade do aluno, com respostas passo a passo em MathML

            Certifique-se de retornar **apenas HTML válido** no componente <div>.
            Não repita as informações passadas, gere apenas os itens 1 e 2.
            """

            # Chamada ao modelo de IA
            response = model.generate_content(prompt).text

            # Adiciona o relatório da dificuldade à lista
            ai_reports.append(f"""
                <div class="difficulty-report border-b pb-4 mb-4">
                    <h3 class="text-lg font-bold">{difficulty.content.title}</h3>
                    <p><strong>Feedback:</strong> {difficulty.feedback}</p>
                    <p><strong>Nível de dificuldade:</strong> {difficulty.level}</p>
                    <div class="ai-suggestions">
                        {response}
                    </div>
                </div>
            """)

        # Renderiza o relatório no template
        return render(request, "report.html", {
            "student": student,
            "report": mark_safe("\n".join(ai_reports)),
            "difficulties": difficulties,
        })

    except Exception as e:
        # Tratamento genérico de erros
        return HttpResponse(f"Erro ao gerar o relatório: {str(e)}", status=500)