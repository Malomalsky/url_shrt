import os
import sys
import json

sys.path.append(os.getcwd())

import unittest
from url_shortener import create_app

from url_shortener.extensions import db, ma
from url_shortener.models import Link


class BasicTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app(config_file='tests/test_settings.py').test_client()
        db.create_all(app=create_app(config_file='tests/test_settings.py'))
    


    def tearDown(self):
        pass
        

    # Tests
    def test_main_page(self):
        response = self.app.get('/links')
        self.assertEqual(response.status_code, 200)

    def test_add_valid_link(self):
        """
        Пробуем добавить валидную ссылку. Проверяем поля в ответе. 
        """
        data = json.dumps({"original_url": "avito.ru"})
        headers = {"Content-Type": "application/json"}
        response = self.app.post('/add_link', data=data, headers=headers, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('short_url', response.json)

        # Тестириуем работоспособность редиректа на добавленную ссылку

        
        
    
    def test_add_not_valid_link(self):
        """
        Пробуем добавить невалидную ссылку.
        """
        data = json.dumps({"original_url": "avito"})
        headers = {"Content-Type": "application/json"}
        response = self.app.post('/add_link', data=data, headers=headers, follow_redirects=True)
        self.assertEqual(response.status_code, 400)

    def test_add_valid_and_custom_links(self):
        """Пробуем добавить валидную ссылку и кастомную ссылку."""
        data = json.dumps({"original_url": "avito.ru", "short_url" : "best"})
        headers = {"Content-Type": "application/json"}
        response = self.app.post('/add_link', data=data, headers=headers, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('short_url', response.json)
        self.assertIn('custom_url', response.json)

    def test_get_link_by_id(self):
        """Получить информацию по id"""
        headers = {"Content-Type": "application/json"}
        response = self.app.get('/links/1', headers=headers)
        self.assertEqual(response.status_code, 200)

    



if __name__ == '__main__':
    unittest.main()
