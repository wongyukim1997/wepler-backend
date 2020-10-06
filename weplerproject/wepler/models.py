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
    plus_class = models.CharField(verbose_name='분야', max_length=50)
    plus_date = models.CharField(verbose_name='요일', max_length=55)
    plus_info = models.TextField(verbose_name='한글소개')
    #한줄소개, 프로필 타입

class Plz(models.Model):
    plz_id = models.EmailField(verbose_name='아이디', max_length=100, primary_key=True)
    plz_password = models.CharField(verbose_name='비밀번호', max_length=100)
    plz_name = models.CharField(verbose_name='이름', max_length=10)
    plz_address_small = models.CharField(verbose_name='주소', max_length=100)
    plz_group = models.CharField(verbose_name='개인/단체', max_length=50)
    plz_phonenumber = models.CharField(verbose_name='전화번호', max_length=15)
    plz_address_big = models.CharField(verbose_name='행정구역', max_length=10)
    plz_when_learn = models.CharField(verbose_name='희망 기간', max_length=50)
    plz_class = models.CharField(verbose_name='분야', max_length=50)
    plz_date = models.CharField(verbose_name='요일', max_length=55)


class Plus_field(models.Model):
    plus_user = models.ForeignKey(Plus, on_delete=models.CASCADE)
    plus_class = models.CharField(verbose_name='이름', max_length=20)

class Plus_day(models.Model):
    plus_user = models.ForeignKey(Plus, on_delete=models.CASCADE)
    plus_date = models.CharField(verbose_name='이름', max_length=10)

class Plz_field(models.Model):
    plz_user = models.ForeignKey(Plz, on_delete=models.CASCADE)
    plz_class = models.CharField(verbose_name='이름', max_length=20)

class Hire_board(models.Model):     #이름 추가하기
    plz_user = models.ForeignKey(Plz, on_delete=models.CASCADE)
    plz_name = models.CharField(verbose_name='이름', max_length=10)
    plz_class = models.CharField(verbose_name='분야', max_length=50)
    title = models.CharField(max_length=20, verbose_name='제목')
    content = models.TextField(verbose_name='내용')
    date = models.DateField(verbose_name='입력 날짜')
    start_date = models.DateField(verbose_name='시작 날짜')
    end_date = models.DateField(verbose_name='끝 날짜')
    recruit = models.DateField(verbose_name='마감일')
    need_member = models.IntegerField(verbose_name='필요인원')
    apply_member = models.IntegerField(verbose_name='신청인원')
    timeover = models.CharField(verbose_name='모집여부', max_length=10)
    plz_group = models.CharField(verbose_name='개인/단체', max_length=50)

class Choice_board(models.Model):
    plus_user = models.ForeignKey(Plus, on_delete=models.CASCADE)
    plus_name = models.CharField(verbose_name='이름', max_length=10)
    plus_address_small = models.CharField(verbose_name='주소', max_length=100)
    plus_phonenumber = models.CharField(verbose_name='전화번호', max_length=15)
    plus_start_time = models.TimeField(verbose_name='시작 시간')
    plus_end_time = models.TimeField(verbose_name='끝 시간')
    plus_continu_month = models.IntegerField(verbose_name='몇개월')
    plus_address_big = models.CharField(verbose_name='행정구역', max_length=10)
    plus_point = models.FloatField(verbose_name='점수')
    plus_class = models.CharField(verbose_name='분야', max_length=50)
    plus_date = models.CharField(verbose_name='요일', max_length=55)
    plus_info = models.TextField(verbose_name='한글소개')
    plus_edu = models.BooleanField(verbose_name='교육 여부', blank = True)

#plz가 plus를 리뷰한것
#date는 date필드로 바꿀것
class Plus_review(models.Model):
    plus_user = models.ForeignKey(Plus, on_delete=models.CASCADE)
    plz_user = models.ForeignKey(Plz, on_delete=models.CASCADE)
    plus_name = models.CharField(verbose_name='이름', max_length=10)
    plz_name = models.CharField(verbose_name='이름', max_length=10)
    plus_class = models.CharField(verbose_name='분야', max_length=50)
    date = models.DateField(verbose_name='입력 날짜')
    title = models.CharField(max_length=20, verbose_name='제목')
    content = models.TextField(verbose_name='내용')
    plus_point = models.FloatField(verbose_name='점수')
    match_id = models.IntegerField(verbose_name='매칭 ID')

#plus가 plz를 리뷰한것
class Plz_review(models.Model):
    plus_user = models.ForeignKey(Plus, on_delete=models.CASCADE)
    plz_user = models.ForeignKey(Plz, on_delete=models.CASCADE)
    plz_class = models.CharField(verbose_name='분야', max_length=50)
    plus_name = models.CharField(verbose_name='이름', max_length=10)
    plz_name = models.CharField(verbose_name='이름', max_length=10)
    date = models.DateField(verbose_name='입력 날짜')
    title = models.CharField(max_length=20, verbose_name='제목')
    content = models.TextField(verbose_name='내용')
    match_id = models.IntegerField(verbose_name='매칭 ID')

#서로의 이름을 알아야함
class Plus_apply(models.Model):
    plz_user = models.ForeignKey(Plz, on_delete=models.CASCADE)
    plus_user = models.ForeignKey(Plus, on_delete=models.CASCADE)
    plus_user_name = models.CharField(verbose_name='이름', max_length=10)
    plz_user_name = models.CharField(verbose_name='이름', max_length=10)
    title = models.CharField(verbose_name='주제', max_length=30)
    plus_address = models.CharField(verbose_name='활동분야(결국 사는곳)', max_length=10)
    plz_address = models.CharField(verbose_name='활동분야(결국 사는곳)', max_length=10)
    plz_class = models.CharField(verbose_name='분야', max_length=50)
    plus_class = models.CharField(verbose_name='분야', max_length=50)
    plus_date = models.CharField(verbose_name='요일', max_length=55)
    hire_id = models.ForeignKey(Hire_board, on_delete=models.CASCADE)
    plus_point = models.FloatField(verbose_name='점수')

#plz가 신청하는 경우
#choice id 추가해야함
#점수 추가
class Plz_apply(models.Model):
    plz_user = models.ForeignKey(Plz, on_delete=models.CASCADE)
    plus_user = models.ForeignKey(Plus, on_delete=models.CASCADE)
    plz_user_name = models.CharField(verbose_name='이름', max_length=10)
    plus_user_name = models.CharField(verbose_name='이름', max_length=10)
    plz_address = models.CharField(verbose_name='활동분야(결국 사는곳)', max_length=10)
    plus_address = models.CharField(verbose_name='활동분야(결국 사는곳)', max_length=10)
    plz_class = models.CharField(verbose_name='분야', max_length=50)
    plus_class = models.CharField(verbose_name='분야', max_length=50)
    plus_date = models.CharField(verbose_name='요일', max_length=55)
    plus_point = models.FloatField(verbose_name='점수')
    choice_id = models.ForeignKey(Choice_board, on_delete=models.CASCADE)

class Match(models.Model):
    plus_user = models.ForeignKey(Plus, on_delete=models.CASCADE)
    plz_user = models.ForeignKey(Plz, on_delete=models.CASCADE)
    plz_name = models.CharField(verbose_name='이름', max_length=10)
    plus_name = models.CharField(verbose_name='이름', max_length=10) 
    plus_class = models.CharField(verbose_name='분야', max_length=50)
    plz_class = models.CharField(verbose_name='분야', max_length=50)
    plus_address_big = models.CharField(verbose_name='행정구역', max_length=10)
    plz_address_big = models.CharField(verbose_name='행정구역', max_length=10)
    match_subject =models.CharField(verbose_name='주제', max_length=20)
    complete = models.BooleanField(verbose_name='완료/진행')
    h_id = models.IntegerField(verbose_name='고용게시글')
