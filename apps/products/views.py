from django.db.models import Min, Max, Sum
from rest_framework import generics, viewsets
from rest_framework.response import Response

from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer
from apps.users.permissions import IsEmployeeOrHigherChange, IsUserOrHigher


class CategoryViewSet(viewsets.ModelViewSet):
    """
    Вьюсет для просмотра и редактирования категорий.
    Только сотрудники и администраторы могут создавать,
    обновлять или удалять категории.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsEmployeeOrHigherChange]


class ProductViewSet(viewsets.ModelViewSet):
    """
    Вьюсет для просмотра и редактирования продуктов.
    Все аутентифицированные пользователи могут просматривать продукты.
    Только сотрудники и администраторы могут создавать,
    обновлять или удалять продукты.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsUserOrHigher, IsEmployeeOrHigherChange]


class ProductListView(generics.ListAPIView):
    """
    API-вью для получения списка продуктов.
    Все аутентифицированные пользователи могут
    просматривать список продуктов с пагинацией.
    """
    queryset = Product.objects.all().order_by('id')
    serializer_class = ProductSerializer


class ProductDetailView(generics.RetrieveAPIView):
    """
    API-вью для получения продукта по его ID.
    Все аутентифицированные пользователи могут просматривать детали продукта.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductsByCategoryView(generics.ListAPIView):
    """
    API-вью для получения списка продуктов в
    конкретнойкатегории и ее подкатегориях.
    Все аутентифицированные пользователи могут просматривать список продуктов.
    """
    serializer_class = ProductSerializer

    def get_queryset(self):
        """
        Этот метод возвращает список всех продуктов,
        принадлежащих к конкретной категории и ее подкатегориям.
        """
        category_name = self.kwargs['category_name']
        category = Category.objects.get(name=category_name)
        return Product.objects.filter(categories=category).order_by('id')


class ProductStatsView(generics.GenericAPIView):
    """
    API-вью для получения статистики по продуктам.
    Возвращает минимальную цену, максимальную цену и
    общий остаток всех продуктов.
    """
    def get(self, request, *args, **kwargs):
        """
        Обрабатывает GET-запрос для получения статистики по продуктам.
        """
        stats = Product.objects.aggregate(
            min_price=Min('regular_price'),
            max_price=Max('regular_price'),
            total_stock=Sum('stock')
        )
        return Response(stats)
