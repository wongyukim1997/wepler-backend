from .models import *
from rest_framework import serializers

class PlusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plus
        fields = '__all__'
    
class PlzSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plz
        fields = '__all__'

class Hire_boardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hire_board
        fields = '__all__'

class Choice_boardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice_board
        fields = '__all__'

class Plus_ApplySerializer(serializers.ModelSerializer):
    class Meta:
        model = Plus_apply
        fields = '__all__'

class Plz_ApplySerializer(serializers.ModelSerializer):
    class Meta:
        model = Plz_apply
        fields = '__all__'

class MatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = '__all__'

class Plus_reviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plus_review
        fields = '__all__'

class Plz_reviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plz_review
        fields = '__all__'