from tempfile import TemporaryDirectory
from pathlib import Path
from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse

from .models import Grade


class GradeSavingTests(TestCase):
    def setUp(self):
        self.data = {
            'student_name': 'Иванов', 'group': 'ИУ-1', 'subject': 'Математика',
            'grade': 5, 'date': '2026-10-26', 'teacher': 'Петров',
            'storage': 'database',
        }

    def test_database_save_and_duplicate(self):
        self.client.post(reverse('index'), self.data)
        response = self.client.post(reverse('index'), {**self.data, 'grade': 4})
        self.assertEqual(Grade.objects.count(), 1)
        self.assertContains(response, 'уже существует')

    def test_file_save(self):
        with TemporaryDirectory() as directory, patch('grades.utils.STORAGE_DIR', Path(directory) / 'storage'):
            for file_format in ('json', 'xml'):
                response = self.client.post(reverse('index'), {
                    **self.data, 'storage': 'file', 'file_format': file_format,
                })
                self.assertContains(response, 'сохранены в файл')
                self.assertEqual(len(list((Path(directory) / 'storage').glob(f'*.{file_format}'))), 1)
        self.assertEqual(Grade.objects.count(), 0)

    def test_invalid_grade(self):
        response = self.client.post(reverse('index'), {**self.data, 'grade': 6})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Grade.objects.count(), 0)
