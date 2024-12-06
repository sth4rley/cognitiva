# forms.py
from django import forms
from .models import Student, Teacher, Classroom, Content, Difficulty

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'age', 'email']

class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['name', 'subject']

class ClassroomForm(forms.ModelForm):
    class Meta:
        model = Classroom
        fields = ['name', 'teacher', 'students']

class ContentForm(forms.ModelForm):
    class Meta:
        model = Content
        fields = ['title', 'classroom', 'description']

class DifficultyForm(forms.ModelForm):
    class Meta:
        model = Difficulty
        fields = ['content', 'level', 'feedback']

    def save(self, commit=True, student=None):
        instance = super().save(commit=False)
        if student:
            instance.student = student
        if commit:
            instance.save()
        return instance
