# models.py
from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name

class Teacher(models.Model):
    name = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Classroom(models.Model):
    name = models.CharField(max_length=100)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='classrooms')
    students = models.ManyToManyField(Student, related_name='classrooms')

    def __str__(self):
        return self.name

class Content(models.Model):
    title = models.CharField(max_length=100)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, related_name='contents', default=1)  # exemplo com id da sala de aula padrão
    description = models.TextField()

    def __str__(self):
        return self.title

class Difficulty(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='difficulties')
    content = models.ForeignKey(Content, on_delete=models.CASCADE, related_name='difficulties')
    level = models.PositiveSmallIntegerField(choices=[(1, 'Low'), (2, 'Medium'), (3, 'High')])
    feedback = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.student.name} - {self.content.title} ({self.level})"
