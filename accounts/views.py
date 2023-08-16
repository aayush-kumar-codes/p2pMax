import base64, os, re

from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.urls import reverse

from admin_material.views import UserLoginView
from admin_material.forms import LoginForm

from .forms import AddBinanceKeyForm, RegistrationForm

from .models import User
from .utils.helper import validate_binance_keys, validate_telegram, validate_password
from .decorator import login_required


# @login_required
# def home(request):
#     return render(request, 'home.html')

@login_required
def index(request):
  if request.user.role == 'admin':
    users_count = User.objects.filter(is_active=True).count()
    users = User.objects.all()
    data = { 'segment': 'index', 'title': 'Dashboard', 'active_users': users_count, 'users': users }
    return render(request, 'pages/index.html', data)
  return render(request, 'pages/home.html', { 'segment': 'index', 'title': 'Dashboard'})

class CustomUserLoginView(UserLoginView):
    template_name = 'accounts/login.html'
    form_class = LoginForm

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/')
        return super().get(request, *args, **kwargs)


def register(request):
  if request.user.is_authenticated:
    return redirect('/')
  if request.method == 'POST':
    form = RegistrationForm(request.POST)
    if form.is_valid():
      form.save()
      print('Account created successfully!')
      return redirect('/accounts/login/')
    else:
      print("Register failed!")
  else:
    form = RegistrationForm()

  context = { 'form': form, 'title': 'Register' }
  return render(request, 'accounts/register.html', context)

@login_required
def user_profile(request):
  user = request.user
  
  if request.method == 'POST':
    #update the user-profile
    if request.POST.get('fname'):
      user.first_name = request.POST['fname']
    if request.POST.get('lname'):
      user.last_name = request.POST['lname']
    if request.POST.get('nick_name'):
      user.nick_name = request.POST['nick_name']
    if request.POST.get('kyc_name'):
      user.kyc_full_name = request.POST['kyc_name']
    if request.POST.get('mobile'):
      user.mobile_no = request.POST['mobile']
    if request.POST.get('country'):
      user.country = request.POST['country']
    if request.POST.get('zip_code'):
      user.zip_code = request.POST['zip_code']
    if request.POST.get('telegram_user'):
      user.telegram_id = request.POST['telegram_user']
       
    user.save()
    messages.success(request, "Success : User updated Successfully!")
    return JsonResponse({
        'success': True,
        'status': 200
    })
   
  return render(request, 'accounts/profile.html', { 'segment': 'profile' })


#def add_binance_key(request):
#  if not request.user.is_authenticated:
#    return redirect('accounts/login')
#  if request.method == 'POST':
#    form = AddBinanceKeyForm(request.POST, instance=request.user)
#    if form.is_valid():
#      form.save()
#      return redirect('/')
#  else:
#    form = AddBinanceKeyForm()
#  
#  context = { 'form': form, 'title': 'Configure' }
#  return render(request, 'accounts/add_binance_key.html', context)

@login_required
def api_management(request):
  user = request.user
  
  if request.method == 'POST':
    form = AddBinanceKeyForm(request.POST, instance=request.user)
    if form.is_valid():
      form.save()
      messages.success(request, "Success : Binance Key added Successfully!")
      return redirect('api_management')
    else:
      messages.error(request, "Error: Please provide a valid binance key!")
      return redirect('api_management')
    
  initial_data = {
    'binance_key': user.binance_key,
    'secret_key': user.secret_key,
  }
  form = AddBinanceKeyForm(initial=initial_data)
  return render(request, 'accounts/api_manage.html', {'form': form})

# @login_required
# def profile_view(request):
#     if request.method == 'GET':
#         user = request.user
#     return render(request, 'profile.html', {'user': user})
      

# @login_required
# def updateprofile_view(request):
#     if request.method == 'GET':
#         user_data = {
#             'kyc_full_name': request.user.kyc_full_name,
#             'nick_name': request.user.nick_name,
#             'mobile_number': request.user.mobile_no,
#             'country': request.user.country,
#             'binance_key': request.user.binance_key,
#             'secret_key': request.user.secret_key,
#             'zip_code': request.user.zip_code,
#         }
#         return render(request, 'editprofile.html', {'user_data': user_data})
    
#     elif request.method == 'POST':
#         user = request.user
#         user.kyc_full_name = request.POST.get('kyc_full_name')
#         user.nick_name = request.POST.get('nick_name')
#         user.mobile_no = request.POST.get('mobile_number')
#         user.country = request.POST.get('country')
#         user.binance_key = request.POST.get('binance_key')
#         user.secret_key = request.POST.get('secret_key')
#         user.zip_code = request.POST.get('zip_code')
#         user.save()
#         messages.success(request, 'Profile updated successfully')
#         return redirect('/profile')

    
# def is_staff_user(user):
#     return user.is_staff

# @login_required
# @user_passes_test(is_staff_user)
# def active_user(request):
#     if request.method == 'GET':
#         active_users = User.objects.filter(is_active=True)
#         return render(request, 'active_users.html', {'active_users': active_users})


# @login_required
# @user_passes_test(is_staff_user)
# def all_users(request):
#     if request.method == 'GET':
#         all_user = User.objects.all()
#         return render(request, 'all_users.html', {'all_user': all_user})
 

# @login_required
# def api_management(request):
#     if request.method == 'GET':
#         user = request.user
#     return render(request, 'api_management.html', {'user': user})
 

# @login_required
# def update_api_management(request):
#     if request.method == 'GET':
#         user_data = {
#             'binance_key': request.user.binance_key,
#             'secret_key': request.user.secret_key,
#         }
#         return render(request, 'editapi_management.html',  {'user_data': user_data})
    
#     elif request.method == 'POST':
#         user = request.user
#         user.binance_key = request.POST.get('binance_key')
#         user.secret_key = request.POST.get('secret_key')
#         if validate_binance_keys(user.binance_key, user.secret_key):
#             user = request.user
#             user.binance_key = user.binance_key
#             user.secret_key = user.secret_key
#             user.save()
#             messages.success(request, 'API Key updated successfully')
#             return redirect('/api-management')
#         else:
#             return redirect('/editapi_management')
