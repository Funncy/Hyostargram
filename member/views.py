from django.shortcuts import render, redirect
from django.contrib.auth import login as django_login, logout as django_logout, authenticate

from .forms import LoginForm, SignUpForm
# Create your views here.

def login(request):
    if request.method == 'POST':
        #로그인 성공후 이동 url
        next = request.GET.get('next')

        # Data bounded form 인스턴스 생성
        #Authentication의 첫 파라미터는 무조건 request
        login_form = LoginForm(request=request, data=request.POST)
        #유효성 검사
        #AuthenticationForm을 사용하면 authenticate과정까지 완료되어야 된다
        if login_form.is_valid():
            user = login_form.get_user()
            '''
            # form 으로부터 아이디 , 비번 가져옴
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']

            #가져온 데이터로 유저가 있는지 판단
            #존재할 경우 인스터스 성생 없으면 None생성
            user = authenticate(
                username=username,
                password=password
            )
            
            #인증 성공
            if user:
                django_login(request, user)

                return redirect('post:post_list')
            #인증 실패
            login_form.add_error(None, '아이디 또는 비밀번호가 올바르지 않습니다.')
            '''
            #장고 auth앱에서 제공해주는 로그인 함수를 실행해 세션을 유지해준다
            django_login(request, user)

            return redirect(next if next else 'post:post_list')
        login_form.add_error(None, '아이디 또는 비밀번호가 올바르지 않습니다.')
    else:  #GET방식 -> 즉 로그인 화면
        login_form = LoginForm()

    ctx = {
        'login_form': login_form,
    }
    return render(request,'member/login.html',ctx)

def logout(request):
    django_logout(request)
    return redirect('post:post_list')

def signup(requset):
    if requset.method == 'POST':
        signup_form = SignUpForm(requset.POST)
        #유효성 검사
        if signup_form.is_valid():
            #유저 생성 후 그 유저 로그인 시킨다.
            user = signup_form.save()
            django_login(requset, user)
            return redirect('post:post_list')
            '''
            #자체 메서드인 signup method실행
            signup_form.signup()
            return redirect('post:post_list')
            '''
    else:
        signup_form = SignUpForm()

    ctx = {
        'signup_form': signup_form,
    }
    return render(requset, 'member/signup.html', ctx)

