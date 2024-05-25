from rest_framework import serializers

from .models import Category, Product


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class ProductSerializer(serializers.ModelSerializer):
    categories = serializers.SlugRelatedField(
        many=True,
        slug_field='name',
        queryset=Category.objects.all()
    )

    class Meta:
        model = Product
        fields = '__all__'

    def validate_regular_price(self, value):
        """Проверка, что обычная цена больше нуля"""
        if value < 0:
            raise serializers.ValidationError(
                "Regular price must be greater than zero."
            )
        return value

    def validate_discount_price(self, value):
        """Проверка, что скидочная цена больше нуля"""
        if value and value < 0:
            raise serializers.ValidationError(
                "Discount price must be greater than zero."
            )
        return value

    def validate_stock(self, value):
        """Проверка, что товарный остаток не отрицательный"""
        if value < 0:
            raise serializers.ValidationError(
                "Stock must be zero or greater."
            )
        return value

    def validate(self, data):
        """Общая проверка данных продукта"""
        regular_price = data.get('regular_price')
        discount_price = data.get('discount_price')

        if discount_price and discount_price >= regular_price:
            raise serializers.ValidationError(
                "Discount price must be less than the regular price."
            )

        return data
