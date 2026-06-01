from django import forms
from .models import Plant, Quiz
class RegisterForm(forms.Form):
    name=forms.CharField(label='Nama',max_length=100)
    username=forms.CharField(label='Username',max_length=100)
    email=forms.EmailField(label='Email')
    password=forms.CharField(label='Password',widget=forms.PasswordInput)
    role=forms.ChoiceField(label='Daftar Sebagai',choices=(('guru','Guru'),('siswa','Siswa')))
class PlantForm(forms.ModelForm):
    class Meta:
        model=Plant
        fields=['name','scientific_name','family','habitat','characteristics','benefits','photo']
        labels={'name':'Nama Tanaman','scientific_name':'Nama Ilmiah','family':'Famili','habitat':'Habitat','characteristics':'Ciri-ciri','benefits':'Manfaat','photo':'Upload Foto Tanaman'}
class QuizForm(forms.ModelForm):
    class Meta:
        model=Quiz
        fields=['question','option_a','option_b','option_c','option_d','correct_answer']
        labels={'question':'Pertanyaan','option_a':'Pilihan A','option_b':'Pilihan B','option_c':'Pilihan C','option_d':'Pilihan D','correct_answer':'Jawaban Benar'}
