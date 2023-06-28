from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect


def register(request):
    """새 사용자를 등록합니다"""
    if request.method != 'POST':
        # 빈 등록 폼을 표시합니다
        form = UserCreationForm()  # (1)
    else:
        # 완성된 폼을 처리합니다
        form = UserCreationForm(data=request.POST)  # (2)

        if form.is_valid():  # (3)
            new_user = form.save()  # (4)
            # 사용자가 로그인하면 홈페이지로 리디렉트합니다
            login(request, new_user)  # (5)
            return redirect('learning_logs:index')  # (6)

    # 빈 폼, 또는 유효하지 않은 폼을 표시합니다
    context = {'form': form}
    return render(request, 'registration/register.html', context)
