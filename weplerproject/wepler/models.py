from django.db import models

class Plus(models.Model):
    plus_id = models.EmailField(verbose_name='아이디', max_length=100, primary_key=True)
    plus_password = models.CharField(verbose_name='비밀번호', max_length=100)
    plus_name = models.CharField(verbose_name='이름', max_length=10)
    plus_edu = models.BooleanField(verbose_name='교육 여부', blank = True)
    plus_address_small = models.CharField(verbose_name='주소', max_length=100)
    plus_phonenumber = models.CharField(verbose_name='전화번호', max_length=15)
    plus_talentshare = models.DateField(verbose_name='시작 날짜')
    plus_start_time = models.TimeField(verbose_name='시작 시간')
    plus_end_time = models.TimeField(verbose_name='끝 시간')
    plus_continu_month = models.IntegerField(verbose_name='몇개월')
    plus_address_big = models.CharField(verbose_name='행정구역', max_length=10)
    plus_oneself = models.TextField(verbose_name='자기소개')
    plus_point = models.FloatField(verbose_name='점수')
    #한줄소개, 프로필 타입
    
class Plus_class(models.Model):
    plus_user = models.ForeignKey(Plus, on_delete=models.CASCADE)
    class_name = models.CharField(verbose_name='분야', max_length=30)

class Plz(models.Model):
    plz_id = models.EmailField(verbose_name='아이디', max_length=100, primary_key=True)
    plz_password = models.CharField(verbose_name='비밀번호', max_length=100)
    plz_name = models.CharField(verbose_name='이름', max_length=10)
    plz_address_small = models.CharField(verbose_name='주소', max_length=100)
    plz_group = models.CharField(verbose_name='개인/단체', max_length=50)
    plz_phonenumber = models.CharField(verbose_name='전화번호', max_length=15)
    plz_address_big = models.CharField(verbose_name='행정구역', max_length=10)
    plz_when_learn = models.CharField(verbose_name='희망 기간', max_length=30)

class Plz_class(models.Model):
    plz_user = models.ForeignKey(Plz, on_delete=models.CASCADE)
    class_name = models.CharField(verbose_name='분야', max_length=30)

class Plus_team(models.Model):
    plus_user = models.ForeignKey(Plus, on_delete=models.CASCADE)
    member_number = models.IntegerField(verbose_name='인원수')

class Hire_board(models.Model):
    plz_user = models.ForeignKey(Plz, on_delete=models.CASCADE)
    plz_class = models.CharField(verbose_name='분야', max_length=50)
    title = models.CharField(max_length=20, verbose_name='제목')
    content = models.TextField(verbose_name='내용')
    date = models.DateTimeField(verbose_name='입력 날짜')
    start_date = models.DateField(verbose_name='시작 날짜')
    end_date = models.DateField(verbose_name='끝 날짜')
    recruit = models.DateField(verbose_name='마감일')
    need_member = models.IntegerField(verbose_name='필요인원')
    apply_member = models.IntegerField(verbose_name='신청인원')

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

class Plus_date(models.Model):
    plus_user = models.ForeignKey(Plus, on_delete=models.CASCADE)
    plus_start_day = models.CharField(verbose_name='요일', max_length=10)

class Plus_apply(models.Model):
    plz_user = models.ForeignKey(Plz, on_delete=models.CASCADE)
    plus_user = models.ForeignKey(Plus, on_delete=models.CASCADE)
    plus_class = models.CharField(verbose_name='분야', max_length=50)
    plus_date = models.ForeignKey(Plus_date, on_delete=models.CASCADE)

class Test_board(models.Model):
    title = models.CharField(verbose_name='제목', max_length=50)
    recruit = models.DateField(verbose_name='모집 기간')
    need_member = models.IntegerField(verbose_name='모집 인원')
    start_date = models.DateField(verbose_name='시작시간')
    end_date = models.DateField(verbose_name='끝시간')
    content = models.TextField(verbose_name='내용')

class Test_fields(models.Model):
    test_board = models.ForeignKey(Test_board, on_delete=models.CASCADE)
    fields = models.CharField(verbose_name='분야', max_length=30)

