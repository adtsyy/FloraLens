import base64
from io import BytesIO
import qrcode
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse
from .decorators import role_required
from .forms import RegisterForm,PlantForm,QuizForm
from .models import Profile,Plant,Quiz,Score
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.db.models import Avg
from django.contrib.auth.models import User
from django.db.models import Sum


def logout_view(request):
    logout(request)
    return redirect('home')

def home(request):
    return render(request,'core/home.html',{'plants':Plant.objects.all().order_by('name')})

def register_view(request):
    if request.method=='POST':
        form=RegisterForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data['username']; email=form.cleaned_data['email']
            if User.objects.filter(username=username).exists(): messages.error(request,'Username sudah digunakan.')
            elif User.objects.filter(email=email).exists(): messages.error(request,'Email sudah digunakan.')
            else:
                user=User.objects.create_user(username=username,email=email,password=form.cleaned_data['password'],first_name=form.cleaned_data['name'])
                Profile.objects.create(user=user,role=form.cleaned_data['role']); login(request,user); return redirect('dashboard')
    else: form=RegisterForm()
    return render(request,'core/register.html',{'form':form})

@login_required
def dashboard(request):
    return redirect('teacher_dashboard' if request.user.profile.role=='guru' else 'student_dashboard')

@role_required('guru')
def teacher_dashboard(request):
    plants = Plant.objects.all().order_by('name')
    scores = Score.objects.select_related('user', 'plant').all()

    total_tanaman = Plant.objects.count()
    total_kuis = Quiz.objects.count()
    total_siswa = Profile.objects.filter(role='siswa').count()

    avg = Score.objects.aggregate(avg=Avg('score'))
    rata_nilai = round(avg['avg'], 1) if avg['avg'] else 0

    siswa_list = Profile.objects.filter(role='siswa').select_related('user')
    leaderboard = []

    for siswa in siswa_list:
        total = Score.objects.filter(user=siswa.user).aggregate(total=Sum('score'))['total'] or 0
        leaderboard.append({
            'nama': siswa.user.first_name or siswa.user.username,
            'total': total
        })

    leaderboard = sorted(leaderboard, key=lambda x: x['total'], reverse=True)

    plant_qr = []
    for plant in plants:
        url = request.build_absolute_uri(reverse('plant_detail', args=[plant.code]))
        img = qrcode.make(url)
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        qr_base64 = base64.b64encode(buffer.getvalue()).decode()
        plant_qr.append({'plant': plant, 'qr': qr_base64, 'url': url})

    return render(request, 'core/teacher_dashboard.html', {
        'plants': plants,
        'scores': scores,
        'plant_qr': plant_qr,
        'total_tanaman': total_tanaman,
        'total_kuis': total_kuis,
        'total_siswa': total_siswa,
        'rata_nilai': rata_nilai,
        'leaderboard': leaderboard,
    })

@role_required('siswa')
def student_dashboard(request):
    return render(request,'core/student_dashboard.html',{'scores':Score.objects.filter(user=request.user).select_related('plant')})

@login_required
def plant_detail(request,code):
    plant=get_object_or_404(Plant,code=code); quizzes=plant.quizzes.all()
    if request.method=='POST' and request.user.profile.role=='siswa':
        total=quizzes.count(); correct=0
        for quiz in quizzes:
            if request.POST.get(f'quiz_{quiz.id}')==quiz.correct_answer: correct+=1
        score=round((correct/total)*100) if total>0 else 0
        Score.objects.create(user=request.user,plant=plant,score=score); messages.success(request,f'Kuis berhasil dikirim. Skor kamu: {score}')
    return render(request,'core/plant_detail.html',{'plant':plant,'quizzes':quizzes})

@role_required('siswa')
def scan_qr(request): return render(request,'core/scan.html')

@role_required('guru')
def plant_add(request):
    form=PlantForm(request.POST or None, request.FILES or None)
    if request.method=='POST' and form.is_valid(): form.save(); messages.success(request,'Tanaman berhasil ditambahkan.'); return redirect('teacher_dashboard')
    return render(request,'core/form.html',{'form':form,'title':'Tambah Tanaman','back_url':'teacher_dashboard'})

@role_required('guru')
def plant_edit(request,pk):
    plant=get_object_or_404(Plant,pk=pk); form=PlantForm(request.POST or None,request.FILES or None,instance=plant)
    if request.method=='POST' and form.is_valid(): form.save(); messages.success(request,'Tanaman berhasil diperbarui.'); return redirect('teacher_dashboard')
    return render(request,'core/form.html',{'form':form,'title':'Edit Tanaman','back_url':'teacher_dashboard'})

@role_required('guru')
def plant_delete(request,pk):
    plant=get_object_or_404(Plant,pk=pk)
    if request.method=='POST': plant.delete(); messages.success(request,'Tanaman berhasil dihapus.'); return redirect('teacher_dashboard')
    return render(request,'core/confirm_delete.html',{'object_name':plant.name,'back_url':'teacher_dashboard'})

@role_required('guru')
def quiz_manage(request,plant_id):
    plant=get_object_or_404(Plant,pk=plant_id); return render(request,'core/quiz_manage.html',{'plant':plant,'quizzes':plant.quizzes.all()})

@role_required('guru')
def quiz_add(request,plant_id):
    plant=get_object_or_404(Plant,pk=plant_id); form=QuizForm(request.POST or None)
    if request.method=='POST' and form.is_valid(): quiz=form.save(commit=False); quiz.plant=plant; quiz.save(); messages.success(request,'Kuis berhasil ditambahkan.'); return redirect('quiz_manage',plant_id=plant.id)
    return render(request,'core/form.html',{'form':form,'title':f'Tambah Kuis - {plant.name}','back_url':'quiz_manage','back_arg':plant.id})

@role_required('guru')
def quiz_edit(request,pk):
    quiz=get_object_or_404(Quiz,pk=pk); form=QuizForm(request.POST or None,instance=quiz)
    if request.method=='POST' and form.is_valid(): form.save(); messages.success(request,'Kuis berhasil diperbarui.'); return redirect('quiz_manage',plant_id=quiz.plant.id)
    return render(request,'core/form.html',{'form':form,'title':'Edit Kuis','back_url':'quiz_manage','back_arg':quiz.plant.id})

@role_required('guru')
def quiz_delete(request,pk):
    quiz=get_object_or_404(Quiz,pk=pk); plant_id=quiz.plant.id
    if request.method=='POST': quiz.delete(); messages.success(request,'Kuis berhasil dihapus.'); return redirect('quiz_manage',plant_id=plant_id)
    return render(request,'core/confirm_delete.html',{'object_name':quiz.question,'back_url':'quiz_manage','back_arg':plant_id})

@role_required('guru')
def score_delete(request,pk):
    score=get_object_or_404(Score,pk=pk)
    if request.method=='POST': score.delete(); messages.success(request,'Nilai berhasil dihapus.')
    return redirect('teacher_dashboard')
