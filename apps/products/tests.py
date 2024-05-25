from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from .models import Category, Product
from apps.users.models import User


class ProductTests(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.employee_user = User.objects.create_user(
            username='employeeuser',
            email='employee@example.com',
            password='employeepassword123',
            role=User.EMPLOYEE
        )
        self.user = User.objects.create_user(
            username='normaluser',
            email='user@example.com',
            password='userpassword123',
            role=User.USER
        )
        self.category_1 = Category.objects.create(name='Electronics')
        self.category_2 = Category.objects.create(name='Knight equipment')
        self.product_1 = Product.objects.create(
            name='Laptop',
            regular_price='1000.00',
            discount_price='900.00',
            stock=50,
            description='Cool Laptop'
        )
        self.product_2 = Product.objects.create(
            name='Sword',
            regular_price='500.00',
            discount_price='200.00',
            stock=2,
            description='Cool Sword'
        )
        self.product_1.categories.add(self.category_1)
        self.product_2.categories.add(self.category_2)
        self.create_product_url = reverse('product-list')
        self.product_detail_url = reverse(
            'product-detail', kwargs={'pk': self.product_1.pk}
        )

    def test_create_category(self):
        """
        Тестирует создание новой категории сотрудником.
        Проверяет, что категория успешно создана.
        """
        self.client.force_authenticate(user=self.employee_user)
        data = {"name": "Books"}
        response = self.client.post(
            reverse('category-list'), data, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'Books')

    def test_create_product(self):
        """
        Тестирует создание нового продукта сотрудником.
        Проверяет, что продукт успешно создан.
        """
        self.client.force_authenticate(user=self.employee_user)
        data = {
            "name": "Smartphone",
            "regular_price": "700.00",
            "discount_price": "650.00",
            "stock": 100,
            "description": "A new smartphone",
            "categories": [self.category_1.name]
        }
        response = self.client.post('/products/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'Smartphone')

    def test_get_product_list(self):
        """
        Тестирует получение списка продуктов аутентифицированным пользователем.
        Проверяет, что возвращается список продуктов.
        """
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.create_product_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)

    def test_get_product_detail(self):
        """
        Тестирует получение детальной информации о продукте
        аутентифицированным пользователем.
        Проверяет, что возвращается информация о продукте.
        """
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.product_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Laptop')

    def test_get_products_by_category(self):
        """
        Тестирует получение списка продуктов в конкретных категориях.
        Проверяет, что возвращается список продуктов,
        относящихся к указанным категориям.
        """
        self.client.force_authenticate(user=self.user)

        url_laptop = reverse(
            'products-by-category',
            kwargs={'category_name': 'Electronics'}
        )
        response_laptop = self.client.get(url_laptop)
        self.assertEqual(response_laptop.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response_laptop.data['results']), 0)
        if len(response_laptop.data['results']) > 0:
            self.assertEqual(
                response_laptop.data['results'][0]['name'], 'Laptop'
            )

        url_sword = reverse(
            'products-by-category',
            kwargs={'category_name': 'Knight equipment'}
        )
        response_sword = self.client.get(url_sword)
        self.assertEqual(response_sword.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response_sword.data['results']), 0)
        if len(response_sword.data['results']) > 0:
            self.assertEqual(
                response_sword.data['results'][0]['name'], 'Sword'
            )

    def test_get_product_stats(self):
        """
        Тестирует получение статистики по продуктам.
        Проверяет, что возвращаются минимальная цена,
        максимальная цена и общий остаток.
        """
        self.client.force_authenticate(user=self.user)
        url = reverse('product-stats')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('min_price', response.data)
        self.assertIn('max_price', response.data)
        self.assertIn('total_stock', response.data)
