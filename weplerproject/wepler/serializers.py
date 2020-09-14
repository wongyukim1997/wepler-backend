from .models import *
from rest_framework import serializers

class PlusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plus
        fields = '__all__'

class Plus_classSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plus_class
        fields = '__all__'
    
class PlzSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plz
        fields = '__all__'

class Plz_classSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plz_class
        fields = '__all__'

class Test_boardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test_board
        fields = '__all__'