FLORALENS DJANGO

CARA MENJALANKAN:
1. Extract ZIP
2. cd floralens_django
3. python -m venv venv
4. venv\Scripts\activate
5. pip install -r requirements.txt
6. python manage.py makemigrations
7. python manage.py migrate
8. python manage.py runserver
9. Buka http://127.0.0.1:8000

Fitur:
- Register/Login role Guru dan Siswa
- Guru CRUD tanaman dan kuis
- Upload foto tanaman
- QR Code otomatis
- Siswa scan QR dan mengerjakan kuis
- Dashboard guru melihat nilai siswa
- Database SQLite, tidak perlu XAMPP
