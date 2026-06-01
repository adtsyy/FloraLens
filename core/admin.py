from django.contrib import admin
from .models import Profile, Plant, Quiz, Score

# Registrasi model ke Django Admin
admin.site.register(Profile)
admin.site.register(Plant)
admin.site.register(Quiz)
admin.site.register(Score)