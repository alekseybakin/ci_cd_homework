import unittest
import sys
import os
from app import app

class TestRectangleAreaCalculator(unittest.TestCase):
    """Тесты для приложения расчета площади прямоугольника"""
    
    def setUp(self):
        """Настройка тестового клиента Flask"""
        self.app = app.test_client()
        self.app.testing = True
    
    def test_index_page(self):
        """Тест доступности главной страницы"""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        # Проверяем декодированный текст
        decoded_response = response.data.decode('utf-8')
        self.assertIn('Расчет площади прямоугольника', decoded_response)
        self.assertIn('Длина прямоугольника', decoded_response)
        self.assertIn('Ширина прямоугольника', decoded_response)
        self.assertIn('Рассчитать площадь', decoded_response)
    
    def test_calculate_area_post_valid_data(self):
        """Тест расчета площади с корректными данными"""
        test_cases = [
            {'length': '5', 'width': '3', 'expected': '15'},
            {'length': '10.5', 'width': '2.5', 'expected': '26.25'},
            {'length': '0', 'width': '10', 'expected': '0'},
            {'length': '7.7', 'width': '2', 'expected': '15.4'},
        ]
        
        for test in test_cases:
            with self.subTest(test=test):
                response = self.app.post('/calculate', data={
                    'length': test['length'],
                    'width': test['width']
                })
                
                self.assertEqual(response.status_code, 200)
                decoded_response = response.data.decode('utf-8')
                self.assertIn(f'Площадь прямоугольника: <strong>{test["expected"]}</strong>', decoded_response)
    
    def test_calculate_area_get_request(self):
        """Тест GET запроса на страницу расчета"""
        response = self.app.get('/calculate')
        self.assertEqual(response.status_code, 200)
        decoded_response = response.data.decode('utf-8')
        self.assertIn('Длина прямоугольника', decoded_response)
    
    def test_calculate_area_invalid_data(self):
        """Тест обработки некорректных данных"""
        invalid_cases = [
            {'length': 'abc', 'width': '10'},      # Нечисловое значение
            {'length': '', 'width': '10'},         # Пустое значение
            {'length': '5', 'width': 'xyz'},       # Нечисловое значение
            {'length': '5,2', 'width': '3'},       # Неправильный формат числа
        ]
        
        for data in invalid_cases:
            with self.subTest(data=data):
                response = self.app.post('/calculate', data=data)
                self.assertEqual(response.status_code, 200)
                decoded_response = response.data.decode('utf-8')
                self.assertIn('Ошибка: введите числовые значения', decoded_response)
    
    def test_calculate_area_negative_numbers(self):
        """Тест расчета с отрицательными числами"""
        response = self.app.post('/calculate', data={
            'length': '-5',
            'width': '3'
        })
        self.assertEqual(response.status_code, 200)
        decoded_response = response.data.decode('utf-8')
        self.assertIn('<strong>-15</strong>', decoded_response)
    
    def test_form_preserves_input_values(self):
        """Тест сохранения введенных значений в форме после отправки"""
        response = self.app.post('/calculate', data={
            'length': '12.5',
            'width': '4.2'
        })
        
        self.assertEqual(response.status_code, 200)
        decoded_response = response.data.decode('utf-8')
        self.assertIn('value="12.5"', decoded_response)
        self.assertIn('value="4.2"', decoded_response)
    
    def test_calculate_area_large_numbers(self):
        """Тест расчета с большими числами"""
        response = self.app.post('/calculate', data={
            'length': '1000000',
            'width': '500000'
        })
        
        self.assertEqual(response.status_code, 200)
        decoded_response = response.data.decode('utf-8')
        self.assertIn('<strong>500000000000</strong>', decoded_response)
    
    def test_html_structure(self):
        """Тест наличия основных HTML элементов"""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        
        decoded_response = response.data.decode('utf-8')
        # Проверяем наличие важных HTML элементов
        self.assertIn('<!DOCTYPE html>', decoded_response)
        self.assertIn('<form', decoded_response)
        self.assertIn('method="POST"', decoded_response)
        self.assertIn('action="/calculate"', decoded_response)
        self.assertIn('type="number"', decoded_response)
        self.assertIn('required', decoded_response)
    
    def test_response_headers(self):
        """Тест заголовков ответа"""
        response = self.app.get('/')
        self.assertIn('text/html', response.content_type)
        self.assertTrue(response.content_length > 0)

class TestCalculationLogic(unittest.TestCase):
    """Тесты для логики расчета площади"""
    
    def test_area_calculation(self):
        """Тест математической логики расчета площади"""
        test_cases = [
            (5, 3, 15),
            (10.5, 2, 21.0),
            (0, 100, 0),
            (-3, 4, -12),
            (7.7, 2.2, 16.94),
        ]
        
        for length, width, expected in test_cases:
            with self.subTest(length=length, width=width):
                result = length * width
                self.assertAlmostEqual(result, expected, places=2)
    
    def test_string_conversion(self):
        """Тест преобразования строк в числа"""
        test_cases = [
            ('5', '3', 15),
            ('10.5', '2.5', 26.25),
            ('0', '10', 0),
        ]
        
        for str_length, str_width, expected in test_cases:
            with self.subTest(str_length=str_length, str_width=str_width):
                length = float(str_length)
                width = float(str_width)
                result = length * width
                self.assertAlmostEqual(result, expected, places=2)

def run_tests():
    """Запуск всех тестов с подробным выводом"""
    suite = unittest.TestLoader().loadTestsFromTestCase(TestRectangleAreaCalculator)
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestCalculationLogic))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Выход с кодом 1 если были неудачные тесты
    sys.exit(0 if result.wasSuccessful() else 1)

if __name__ == '__main__':
    run_tests()