from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
ROLE_CHOICES=(('guru','Guru'),('siswa','Siswa'))
ANSWER_CHOICES=(('A','A'),('B','B'),('C','C'),('D','D'))

class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    role=models.CharField(max_length=10,choices=ROLE_CHOICES)
    def __str__(self): return f'{self.user.username} - {self.role}'

class Plant(models.Model):
    code=models.SlugField(max_length=100,unique=True,blank=True)
    name=models.CharField(max_length=100)
    scientific_name=models.CharField(max_length=150)
    family=models.CharField(max_length=100)
    habitat=models.TextField()
    characteristics=models.TextField()
    benefits=models.TextField()
    photo=models.ImageField(upload_to='plants/',blank=True,null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    def save(self,*args,**kwargs):
        if not self.code: self.code=slugify(self.name)
        super().save(*args,**kwargs)
    def __str__(self): return self.name

class Quiz(models.Model):
    plant=models.ForeignKey(Plant,on_delete=models.CASCADE,related_name='quizzes')
    question=models.TextField()
    option_a=models.CharField(max_length=255)
    option_b=models.CharField(max_length=255)
    option_c=models.CharField(max_length=255)
    option_d=models.CharField(max_length=255)
    correct_answer=models.CharField(max_length=1,choices=ANSWER_CHOICES)
    def __str__(self): return self.question[:60]
    
class Score(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    plant=models.ForeignKey(Plant,on_delete=models.CASCADE)
    score=models.IntegerField()
    created_at=models.DateTimeField(auto_now_add=True)
    class Meta: ordering=['-created_at']
    def __str__(self): return f'{self.user.username} - {self.plant.name} - {self.score}'
