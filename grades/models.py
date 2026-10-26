from django.db import models


class Grade(models.Model):
    student_name = models.CharField('Имя студента', max_length=100)
    group = models.CharField('Группа', max_length=20)
    subject = models.CharField('Предмет', max_length=100)
    grade = models.PositiveSmallIntegerField('Оценка')
    date = models.DateField('Дата сдачи')
    teacher = models.CharField('Преподаватель', max_length=100)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['student_name', 'group', 'subject', 'date', 'teacher'],
                name='unique_student_subject_grade',
            )
        ]
        ordering = ['-date', 'student_name']

    def __str__(self):
        return f'{self.student_name}: {self.subject}'

# Create your models here.
