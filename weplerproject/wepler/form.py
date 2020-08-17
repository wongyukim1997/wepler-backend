from django import forms
from .models import Plz, Plus, Plus_team, Match, Plus_review, Plz_review, Hire_board 

class PlusForm(forms.ModelForm):
    start_date = forms.DateTimeField(
        label='Start',
        widget=forms.widgets.DateInput(attrs={'type':'date'}),
    )
    end_date = forms.DateTimeField(
        label='End',
        widget=forms.widgets.DateInput(attrs={'type':'date'})
    )
    password = forms.CharField(
        widget=forms.widgets.PasswordInput(attrs={'class': 'form-control'})
    )
    class Meta:
        model = Plus
        fields = '__all__'

class PlzForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.widgets.PasswordInput(attrs={'class': 'form-control'})
    )
    class Meta:
        model = Plz
        fields = '__all__'

class MatchForm(forms.ModelForm):
    class Meta:
        model = Match
        fields = '__all__'

class Plus_teamForm(forms.ModelForm):
    class Meta:
        model = Plus_team
        fields = '__all__'

class Plus_reviewForm(forms.ModelForm):
    start_date = forms.DateTimeField(
        label='Start',
        widget=forms.widgets.DateInput(attrs={'type':'date'}),
    )
    end_date = forms.DateTimeField(
        label='End',
        widget=forms.widgets.DateInput(attrs={'type':'date'})
    )
    class Meta:
        model = Plus_review
        fields = '__all__'

class Plz_reviewForm(forms.ModelForm):
    start_date = forms.DateTimeField(
        label='Start',
        widget=forms.widgets.DateInput(attrs={'type':'date'}),
    )
    end_date = forms.DateTimeField(
        label='End',
        widget=forms.widgets.DateInput(attrs={'type':'date'})
    )
    class Meta:
        model = Plz_review
        fields = '__all__'

class Hire_boardForm(forms.ModelForm):
    start_date = forms.DateTimeField(
        label='Start',
        widget=forms.widgets.DateInput(attrs={'type':'date'}),
    )
    end_date = forms.DateTimeField(
        label='End',
        widget=forms.widgets.DateInput(attrs={'type':'date'})
    )
    class Meta:
        model = Hire_board
        fields = '__all__'