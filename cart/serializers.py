from rest_framework import serializers
from order.models import Order


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'book_id', 'quantity']


class GetCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class EditCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['quantity']
