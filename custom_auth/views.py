from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.conf import settings

# Custom
from .forms import CustomUserLoginForm

UserModel = get_user_model()


@user_passes_test(lambda user: user.is_anonymous, login_url='/', redirect_field_name=None)
def login_view(request):

    if request.method == 'POST':
        form = CustomUserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = None
            try:
                email = validate_email(username)
            except ValidationError as e:
                print("Bad Email:", e)

            password = form.cleaned_data.get('password')

            user = authenticate(email=email, username=username, password=password)
            if user is not None:
                login(request, user, backend=settings.AUTHENTICATION_BACKENDS[0])
                username = request.user
                messages.success(request, f'Logged in as {username}')
                return redirect('home')
            else:
                user = None
                try:
                    user = UserModel.objects.get(username=username)
                except UserModel.DoesNotExist as e:
                    print('User does not exist...')
                
                if user.is_active is False:
                    messages.error(request, 'Something went wrong. Could not log in.')
                    return redirect('auth:login')

    else:
        form = CustomUserLoginForm()


    context = {'form': form, 'active': 'login'}
    return render(request, 'custom_auth/login.html', context)


@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'Successfully logged out!')
    return redirect('home')