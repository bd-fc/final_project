from django.shortcuts import render
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from user.forms import LoginForm, RegisterForm

# Create your views here.

User = get_user_model()

def index(request):
    return render(request, "index.html")

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/login")
    else:
        logout(request)
        form = RegisterForm()
    return render(request, "register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        # TODO: 1. /login로 접근하면 로그인 페이지를 통해 로그인이 되게 해주세요
        # TODO: 2. login 할 때 form을 활용해주세요						

        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password")
            # user = authenticate(username=username, password=raw_password)
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                pass
            else:
                if user.check_password(raw_password):
                    login(request, user)
                    return HttpResponseRedirect("/")
    else:
        form = LoginForm()

    print(form)
    return render(request, "login.html", {"form": form})


def logout_view(request):
    # TODO: 3. /logout url을 입력하면 로그아웃 후 / 경로로 이동시켜주세요						
    logout(request)
    
    # return HttpResponseRedirect("/login")     # 이 코드를 왜 작성해 놓으신건가요? 수정해라고 작성해 놓으신건지? 헷갈리게 해놓으셨네요! ㅜㅜ
    return HttpResponseRedirect("/")


# TODO: 8. user 목록은 로그인 유저만 접근 가능하게 해주세요
@login_required
def user_list_view(request):
    # TODO: 7. /users 에 user 목록을 출력해주세요
    # TODO: 9. user 목록은 pagination이 되게 해주세요
    page = int(request.GET.get("page", 1))
    # users = Users.objects.all().order_by("id")    # order_by('id') : Ascending
    users = User.objects.all().order_by("id")  # order_by('-id') : Descending
    # users = Users.objects.all().order_by("full_name", "-id")     # multi-column
    paginator = Paginator(users, 10)  # list per page
    users = paginator.get_page(page)

    return render(request, "users.html", {"users": users})
