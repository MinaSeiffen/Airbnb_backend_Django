from rest_framework import serializers
from .models import Property, Reservation
from useraccount.serializers import UserDetailSerializer


class PropertiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = [
            'id',
            'title',
            'price_per_night',
            'image_url',
        ]


class PropertiesDetailSerializer(serializers.ModelSerializer):
    land_lord = UserDetailSerializer(many=False, read_only=True)

    class Meta:
        model = Property
        fields = [
            'id',
            'title',
            'description',
            'price_per_night',
            'bedrooms',
            'bathrooms',
            'guests',
            'country',
            'country_code',
            'category',
            'image_url',
            'land_lord',
        ]


class ReservationListSerializer(serializers.ModelSerializer):
    property = PropertiesSerializer(many=False, read_only=True)

    class Meta:
        model = Reservation
        fields = (
            'id',
            'start_date',
            'end_date',
            'number_of_nights',
            'total_price',
            'property',
        )