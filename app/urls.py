from django.urls import path
from . import views

urlpatterns = [
    path('classrooms/', views.list_classrooms, name='list_classrooms'),
    path('students/', views.list_students, name='list_students'),
    path('teachers/', views.list_teachers, name='list_teachers'),
    path('content/add/', views.add_content, name='add_content'),
    path('content/', views.list_content, name='list_content'),  # Nova URL para listar conteúdos
    path('students/add/', views.add_student, name='add_student'),
    path('teachers/add/', views.add_teacher, name='add_teacher'),
    path('classrooms/add/', views.add_classroom, name='add_classroom'),
    path('students/<int:student_id>/difficulties/add/', views.add_difficulty, name='add_difficulty'),
    path('students/<int:id>/report/', views.generate_report_view, name='generate_report'),
    path('edit_difficulty/<int:id>/', views.edit_difficulty, name='edit_difficulty'),
    path('', views.home_view, name='home'),  # A tela inicial
]
