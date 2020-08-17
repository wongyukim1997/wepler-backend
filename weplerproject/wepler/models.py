from django.db import models

class Plus(models.Model):
    plus_id = models.EmailField(verbose_name='아이디', max_length=20)
    plus_password = models.CharField(verbose_name='비밀번호', max_length=20)
    plus_name = models.CharField(verbose_name='이름', max_length=10)
    Class = (
        ('exercise', '운동'),
        ('music', '음악'),
        ('study', '공부'),
    )
    plus_class = models.CharField(verbose_name='분야', max_length=8, choices=Class)
    plus_edu = models.BooleanField(verbose_name='교육 여부')
    plus_start_date = models.DateTimeField(verbose_name='시작 날짜')
    plus_end_date = models.DateTimeField(verbose_name='끝 날짜')
    plus_address = models.CharField(verbose_name='주소', max_length=30)
    plus_has_team = models.BooleanField(verbose_name='팀 여부')
    Job = (
        ('student', '학생'),
        ('worker', '직장인'),
    )
    plus_job = models.CharField(verbose_name='직업', max_length=7, choices=Job)
    

class Plz(models.Model):
    plz_id = models.EmailField(verbose_name='아이디', max_length=20)
    plz_password = models.CharField(verbose_name='비밀번호', max_length=20)
    plz_name = models.CharField(verbose_name='이름', max_length=10)
    Class = (
        ('exercise', '운동'),
        ('music', '음악'),
        ('study', '공부'),
    )
    plz_class = models.CharField(verbose_name='분야', max_length=8, choices=Class)
    plz_address = models.CharField(verbose_name='주소', max_length=30)
    plz_group = models.BooleanField(verbose_name='개인/단체')

class Plus_team(models.Model):
    plus_user = models.ForeignKey(Plus, on_delete=models.CASCADE)
    member_number = models.IntegerField(verbose_name='인원수')

class Hire_board(models.Model):
    plus_user = models.ForeignKey(Plus, on_delete=models.CASCADE)
    plz_user = models.ForeignKey(Plz, on_delete=models.CASCADE)
    title = models.CharField(max_length=20, verbose_name='제목')
    content = models.TextField(verbose_name='내용')
    date = models.DateTimeField(verbose_name='입력 날짜')
    start_date = models.DateTimeField(verbose_name='시작 날짜')
    end_date = models.DateTimeField(verbose_name='끝 날짜')
    h_number = models.IntegerField(verbose_name='필요인원')

class Match(models.Model):
    plus_user = models.ForeignKey(Plus, on_delete=models.CASCADE)
    plz_user = models.ForeignKey(Plz, on_delete=models.CASCADE)
    match_subject = models.CharField(verbose_name='주제', max_length=20)
    complete = models.BooleanField(verbose_name='완료/진행')

class Plus_review(models.Model):
    plus_user = models.ForeignKey(Plus, on_delete=models.CASCADE)
    plz_user = models.ForeignKey(Plz, on_delete=models.CASCADE)
    date = models.DateTimeField(verbose_name='입력 날짜')
    title = models.CharField(max_length=20, verbose_name='제목')
    content = models.TextField(verbose_name='내용')

class Plz_review(models.Model):
    plus_user = models.ForeignKey(Plus, on_delete=models.CASCADE)
    plz_user = models.ForeignKey(Plz, on_delete=models.CASCADE)
    date = models.DateTimeField(verbose_name='입력 날짜')
    title = models.CharField(max_length=20, verbose_name='제목')
    content = models.TextField(verbose_name='내용')
