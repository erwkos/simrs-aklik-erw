import base64
from datetime import datetime, timedelta
# from captcha.fields import CaptchaStore
from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url
import pytz
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from captcha.fields import CaptchaField
from django.conf import settings
from django.contrib import auth, messages
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, SetPasswordForm
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db.models import F
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from .decorators import permissions, check_device
from .forms import (
    UserLoginForm, FormGroupChange, FormGroupNew,
    FormNewUser, CaptchaForm, FormNewFaskesUser, AddUserFaskesForm, IsStaffForm, IsActiveForm
)
from .models import User
from faskes.models import Faskes, KantorCabang


@login_required
@check_device
def dashboard(request):
    # user_device = request.user.meta
    # user_agent = request.META['HTTP_USER_AGENT'].__str__()
    # remote_addr = request.META['REMOTE_ADDR'].__str__()
    # try:
    #     remote_port = request.META['REMOTE_PORT'].__str__()
    # except:
    #     remote_port = ''
    # current_device = user_agent + remote_addr + remote_port
    # print(user_device)
    # print(current_device)
    # print(user_device==current_device)
    # if user_device != current_device:
    #     return HttpResponse("Akses terlarang!")
    return render(request, 'dashboard.html', {})


# def user_login(request):
#     fields = ('username', 'password')
#     login_form = UserLoginForm()
#     if request.method == 'POST':
#         print('post')
#         login_form = UserLoginForm(data=request.POST)
#         print(request.POST.get('username'))
#         if login_form.is_valid():
#             print('valid')
#             try:
#                 user = User.objects.get(username=login_form.cleaned_data.get('username'))
#                 if user.login_is_blocked():
#                     login_form.add_error(field=None, error=f'Login blocked sampai {user.block_login_time}')
#                     return render(request, 'user/login.html', {'login_form': login_form})
#             except ObjectDoesNotExist:
#                 user = None
#             if user is None:
#                 for field in fields:
#                     login_form.add_error(field=field, error='username dan password salah.')
#             elif not user.check_password(login_form.cleaned_data.get('password')):
#                 print('check pass')
#                 if user.login_attempt >= 5:
#                     user.login_attempt = 0
#                     user.blocked_count = F('blocked_count') + 1
#                     user.save()
#                     user.refresh_from_db()
#                     user.block_login_time = datetime.now(pytz.timezone(settings.TIME_ZONE)) + timedelta(minutes=3*user.blocked_count)
#                     user.save()
#                     login_form.add_error(field=None, error=f'Login blocked {user.block_login_time}')
#                     return render(request, 'user/login.html', {'login_form': login_form})
#                 else:
#                     user.login_attempt = F('login_attempt') + 1
#                     user.save()
#                 for field in fields:
#                     login_form.add_error(field=field, error='username dan password salah.')
#             else:
#                 user.is_blocked = False
#                 user.login_attempt = 0
#                 user.blocked_count = 0
#                 user.block_login_time = None
#
#                 # Key yang digunakan untuk enkripsi dan dekripsi
#                 derived_key = base64.b64decode("XxfjQ2pEXmiy/nNZvEJ43i8hJuaAnzbA1Cbn1hOuAgA=")
#                 iv = "1020304050607087".encode('utf-8')
#
#                 # Dekripsi username yang di-post
#                 encrypted_username = base64.b64decode(login_form.cleaned_data.get('username'))
#                 print(login_form.cleaned_data.get('username'))
#                 decrypted_username = decrypt_aes(encrypted_username, derived_key, iv)
#                 username = decrypted_username.decode('utf-8')
#
#                 # Dekripsi username yang di-post
#                 encrypted_password = base64.b64decode(login_form.cleaned_data.get('password'))
#                 decrypted_password = decrypt_aes(encrypted_password, derived_key, iv)
#                 password = decrypted_password.decode('utf-8')
#                 user = auth.authenticate(username=username, password=password)
#                 user.save()
#                 login(request, user)
#                 return redirect('dashboard')
#     context = {
#         'login_form': login_form
#     }
#     return render(request, 'user/login.html', context)


def decrypt_aes(encrypted_data, key, iv):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_data = unpad(cipher.decrypt(encrypted_data), AES.block_size)
    return decrypted_data


def user_login(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        try:
            captcha_value = request.POST.get('captcha')
            captcha_key = request.POST.get('captcha_0')
            # Verifikasi captcha
            if CaptchaStore.objects.filter(challenge=captcha_value, hashkey=captcha_key).exists():
                # print(CaptchaStore.objects.filter(challenge=captcha_value, hashkey=captcha_key))
                print("Captcha Benar")
            else:
                # print(CaptchaStore.objects.filter(challenge=captcha_value, hashkey=captcha_key))
                messages.warning(request, "Captcha Salah.")
                # print("Captcha Salah")
                return redirect('/user/login')
            raw_username = request.POST.get('username')
            raw_password = request.POST.get('password')
            # Key yang digunakan untuk enkripsi dan dekripsi
            derived_key = base64.b64decode("XxfjQ2pEXmiy/nNZvEJ43i8hJuaAnzbA1Cbn1hOuAgA=")
            iv = "1020304050607087".encode('utf-8')

            # Enkripsi username yang di-post
            encrypted_username = base64.b64decode(raw_username)
            # Dekripsi password yang di-post
            decrypted_username = decrypt_aes(encrypted_username, derived_key, iv)
            username = decrypted_username.decode('utf-8')

            # Enkripsi password yang di-post
            encrypted_password = base64.b64decode(raw_password)
            # Dekripsi password yang di-post
            decrypted_password = decrypt_aes(encrypted_password, derived_key, iv)
            password = decrypted_password.decode('utf-8')

            username = username
            password = password
            try:
                user = User.objects.get(username=username)
                # print("Kesini gak")
                # print(user)
                if user.login_is_blocked():
                    # Misalnya, Anda memiliki user.block_login_time yang merupakan waktu dalam bentuk timestamp atau timedelta.
                    block_time = user.block_login_time

                    block_time = timezone.localtime(block_time)
                    # Ubah waktu tersebut menjadi format yang lebih manusiawi, misalnya dalam format jam dan menit.
                    formatted_time = block_time
                    if isinstance(block_time, timedelta):
                        hours, remainder = divmod(block_time.seconds, 3600)
                        minutes, _ = divmod(remainder, 60)
                        formatted_time = f"{hours} jam {minutes} menit"
                    elif isinstance(block_time, datetime):
                        formatted_time = block_time.strftime("%H:%M:%S")  # Sesuaikan format sesuai kebutuhan.
                    messages.info(request,
                                  f'Mohon maaf! Username Anda diblokir sampai pukul {formatted_time}. Terima Kasih')
                    return render(request, 'user/login.html', {'login_form': login_form})
            except ObjectDoesNotExist:
                user = None
                # print("malah jadi kesini")
                # print(user)
            if user is None:
                messages.info(request, 'Username dan/atau Password salah!')
            elif not user.check_password(password):
                # print('check pass')
                if user.login_attempt >= 3:
                    user.login_attempt = 0
                    user.blocked_count = F('blocked_count') + 1
                    user.save()
                    user.refresh_from_db()
                    user.block_login_time = datetime.now(pytz.timezone(settings.TIME_ZONE)) + timedelta(
                        minutes=3 * user.blocked_count)
                    user.save()
                    # Misalnya, Anda memiliki user.block_login_time yang merupakan waktu dalam bentuk timestamp atau timedelta.
                    block_time = user.block_login_time

                    # Ubah waktu tersebut menjadi format yang lebih manusiawi, misalnya dalam format jam dan menit.
                    formatted_time = block_time
                    if isinstance(block_time, timedelta):
                        hours, remainder = divmod(block_time.seconds, 3600)
                        minutes, _ = divmod(remainder, 60)
                        formatted_time = f"{hours} jam {minutes} menit"
                    elif isinstance(block_time, datetime):
                        formatted_time = block_time.strftime("%H:%M:%S")  # Sesuaikan format sesuai kebutuhan.
                    messages.info(request,
                                  f'Mohon maaf! Username Anda diblokir sampai pukul {formatted_time}. Terima Kasih')
                    return render(request, 'user/login.html', {'login_form': login_form})
                else:
                    user.login_attempt = F('login_attempt') + 1
                    user.save()
                    messages.info(request, 'Username dan/atau Password salah!')
                    return redirect('/user/login')
            else:
                user = auth.authenticate(username=username, password=password)
                # print("nahloh")
                # print(user)
                if user is not None:
                    user.is_blocked = False
                    user.login_attempt = 0
                    user.blocked_count = 0
                    user.block_login_time = None

                    # Set session ID dan perangkat pada pengguna
                    user_agent = request.META['HTTP_USER_AGENT'].__str__()
                    remote_addr = request.META['REMOTE_ADDR'].__str__()
                    try:
                        remote_port = request.META['REMOTE_PORT'].__str__()
                    except:
                        remote_port = ''
                    meta = user_agent + remote_addr #+ remote_port
                    user.meta = meta

                    user.save()
                    auth.login(request, user)
                    # messages.info(request,
                    #               'Selamat datang di VIBI')
                    return redirect('/')
                else:
                    messages.info(request, 'Gagal Login! Username Anda tidak memiliki hak akses pada aplikasi ini.')
                    return redirect('/user/login')
        except Exception as e:
            messages.info(request, 'Username dan/atau Password salah!')
    login_form = UserLoginForm()
    new_captcha = CaptchaStore.generate_key()
    captcha_image = captcha_image_url(new_captcha)
    context = {
        'captcha_key': new_captcha,
        'captcha_image': captcha_image,
        'login_form': login_form,
    }
    # messages.success(request, 'Selamat datang di Aplikasi VIBI')
    return render(request, 'user/login.html', context)


@login_required
@check_device
def ubahpassword(request):
    if request.method == 'POST':
        raw_old_password = request.POST.get('old_password')
        raw_password_1 = request.POST.get('password1')
        raw_password_2 = request.POST.get('password2')
        # Key yang digunakan untuk enkripsi dan dekripsi
        derived_key = base64.b64decode("XxfjQ2pEXmiy/nNZvEJ43i8hJuaAnzbA1Cbn1hOuAgA=")
        iv = "1020304050607087".encode('utf-8')

        # Enkripsi old password  yang di-post
        encrypted_old_password = base64.b64decode(raw_old_password)
        # Dekripsi password yang di-post
        decrypted_old_password = decrypt_aes(encrypted_old_password, derived_key, iv)
        old_password = decrypted_old_password.decode('utf-8')

        # Enkripsi password yang di-post
        encrypted_password_1 = base64.b64decode(raw_password_1)
        encrypted_password_2 = base64.b64decode(raw_password_2)
        # Dekripsi password yang di-post
        decrypted_password_1 = decrypt_aes(encrypted_password_1, derived_key, iv)
        decrypted_password_2 = decrypt_aes(encrypted_password_2, derived_key, iv)
        password_1 = decrypted_password_1.decode('utf-8')
        password_2 = decrypted_password_2.decode('utf-8')

        old_password = old_password
        password_1 = password_1
        password_2 = password_2

        user = authenticate(username=request.user.username, password=old_password)

        if user is not None:
            try:
                validate_password(password_1, password_validators=None)
                # validate_password(password_2, password_validators=None)
            except ValidationError as e:
                messages.warning(request, e)
                return redirect('/user/ubahpassword')
            if old_password == password_1:
                messages.warning(request, 'Password Lama Tidak Boleh Sama dengan Password Baru')
            elif password_1 == password_2:
                user.set_password(password_1)
                user.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Password Berhasil Diubah')
            else:
                messages.warning(request, ' Password Tidak Sama')
        else:
            messages.warning(request, ' Password Lama Salah')

    return render(request, 'user/ubahpassword.html')


@login_required
def user_logout(request):
    auth.logout(request)
    messages.info(request, 'Anda telah Logout! Terima Kasih.')
    return redirect('/user/login')


@login_required
@check_device
@permissions(role=['adminWEB'])
def create_user_kantor_cabang(request):
    """create user
    
    User dengan group `adminWEB` membuat user baru.
    User yang baru dibuat akan tambahkan ke model yang sesuai.
    """
    # user adalah anggota models KantorCabang atau None
    is_cabang = request.user.kantorcabang_set.first() or None

    # user adalah anggota Fakses atau None
    is_faskes = request.user.faskes_set.first() or None

    if request.method == 'POST':
        form = FormNewUser(
            data=request.POST
        )
        if form.is_valid():
            fm = form.save()

            if is_cabang:
                # user login adalah anggota kantor cabang
                # menambahkan user yang baru dibuat menjadi anggota
                # kantor cabang, sesuai dengan adminWEB yang login
                cbg = KantorCabang.objects.get(pk=is_cabang.pk)
                cbg.user.add(fm)
                messages.success(request, f'Username {fm} berhasil dibuat')
                return redirect(reverse_lazy('user:kanca_user_list'))

            if is_faskes:
                # user login anggota Faskes
                # menambahkan user yang baru dibuat menjadi anggota
                # Faskes sesuai dengan adminWEB (user login)
                fks = Faskes.objects.get(
                    pk=is_faskes.pk
                )
                fks.user.add(fm)
                return redirect(reverse_lazy('user:cbg_user_list'))
    else:
        form = FormNewUser()

    context = {
        "form": form
    }
    return render(request, 'user/form.html', context)


@login_required
@check_device
@permissions(role=['adminWEB'])
def create_user_faskes(request):
    faskes = Faskes.objects.filter(kantor_cabang__user=request.user)
    if request.method == 'POST':
        form = FormNewFaskesUser(data=request.POST)
        if form.is_valid():
            # tambah fm ke faskes
            add_faskes = faskes.filter(nama=request.POST.get('faskes')).first()
            if add_faskes is not None:
                try:
                    fm = form.save()
                    add_faskes.user.add(fm)
                    messages.success(request, f'Username {fm} berhasil dibuat')
                    return redirect(request.headers.get('Referer'))
                except Exception as e:
                    messages.warning(request, "Terdapat Error dengan Keterangan :", str(e))
                    return redirect(request.headers.get('Referer'))
            elif add_faskes is None:
                messages.warning(request, "Terdapat Error dengan Keterangan : Tidak ada Faskes")
                return redirect(request.headers.get('Referer'))
    else:
        form = FormNewFaskesUser()
        # form_faskes = AddUserFaskesForm()

    context = {
        'form': form,
        'faskes': faskes,
        # 'form_faskes': form_faskes,
    }
    return render(request, 'user/form_faskes.html', context)


@login_required
@check_device
@permissions(role=['adminWEB'])
def user_per_kanca(request):
    """user_per_faskes
    List user berdasarkan Kantor Cabang
    """
    # initial relasi pada kantor cabang
    related_user = request.user.kantorcabang_set.all()

    # membuat object user
    obj = User.objects.filter(kantorcabang__in=related_user).exclude(groups__name='adminWEB')
    return render(
        request,
        'user/cabang-list.html',
        {
            'object_list': obj,
            'kanca': related_user.first()
        }
    )


@login_required
@check_device
@permissions(role=['adminWEB'])
def user_per_faskes(request):
    """update_user
    Mengubah
    """
    # initial relasi faskes
    related_user = request.user.kantorcabang_set.all().first()

    # membuat object user
    obj = Faskes.objects.filter(kantor_cabang=related_user)

    context = {
        "object_list": obj,
    }
    return render(request, 'user/faskes-list.html', context)


@login_required
@check_device
@permissions(role=['adminWEB'])
def user_per_verifikator(request):
    """user_per_verifikator
    List user berdasarkan Kantor Cabang
    """
    # initial relasi pada kantor cabang
    related_user = request.user.kantorcabang_set.all()

    # membuat object user
    obj = User.objects.filter(kantorcabang__in=related_user, groups__name='verifikator').order_by('-is_staff')

    context = {
        'object_list': obj,
        'kanca': related_user.first()
    }
    return render(request, 'user/verifikator-list.html', context)


@login_required
@check_device
@permissions(role=['adminWEB'])
def change_password(request, pk):
    """change_password
    Mengganti password user oleh `adminWEB`
    """
    queryset = User.objects.filter(kantorcabang=request.user.kantorcabang_set.all().first())
    instance = queryset.get(id=pk)
    # user = User.objects.get(pk=pk)
    name = instance.get_full_name() or instance.username
    if request.method == 'POST':
        form = SetPasswordForm(
            user=instance,
            data=request.POST
        )
        if form.is_valid():
            form.save()
            messages.add_message(
                request,
                messages.SUCCESS,
                f'Password {name} berhasil diubah'
            )
            return redirect(reverse_lazy('user:kanca_user_list'))
    else:
        form = SetPasswordForm(user=instance)
    context = {
        "form": form
    }
    return render(request,'user/ubahpassword.html', context)


@login_required
@check_device
@permissions(role=['adminWEB'])
def change_group(request, pk):
    """change group
    `adminWEB` assign user ke group tertentu
    """
    queryset = User.objects.filter(kantorcabang=request.user.kantorcabang_set.all().first())
    instance = queryset.get(id=pk)
    # user = User.objects.get(pk=pk)
    name = instance.get_full_name() or instance.username
    form = FormGroupChange(instance=instance)
    if request.method == 'POST':
        form = FormGroupChange(data=request.POST)
        if form.is_valid():
            new_groups = form.cleaned_data.get('groups')
            instance.groups.set(new_groups)
            messages.success(request, f"User {name} berhasil diubah group")
            return redirect(reverse_lazy('user:kanca_user_list'))
    context = {
        "form": form,
        "title": name,
    }
    return render(request, 'user/change_user_group.html', context)


@login_required
@check_device
@permissions(role=['adminWEB'])
def add_group(request):
    """add group

    `adminWEB` menambahkan nama group
    """
    if request.method == 'POST':
        form = FormGroupNew(
            request.POST
        )
        if form.is_valid():
            form.save()
    else:
        form = FormGroupNew()

    context = {
        "form": form,
        "title": "Buat Group Baru"
    }
    return render(
        request,
        'user/form.html',
        context
    )


@login_required
@check_device
@permissions(role=['adminWEB'])
def edit_user_verifikator_active(request, pk):
    queryset = User.objects.filter(kantorcabang=request.user.kantorcabang_set.all().first())
    instance = queryset.get(id=pk)
    # user = User.objects.get(pk=pk)
    form = IsActiveForm(instance=instance)
    if request.method == 'POST':
        form = IsActiveForm(data=request.POST, instance=instance)
        if form.is_valid():
            form.save()
            messages.success(request, 'Status Active berhasil diubah')
            return redirect('user:user_per_verifikator')
        else:
            form = IsActiveForm()
            messages.warning(request, 'Status Active tidak berhasil diubah')

    content = {
        'form': form,
        'instance': instance,
    }
    return render(request, 'staff/edit_user_verifikator.html', content)


@login_required
@check_device
@permissions(role=['adminWEB'])
def edit_user_verifikator_staff(request, pk):
    queryset = User.objects.filter(kantorcabang=request.user.kantorcabang_set.all().first())
    instance = queryset.get(id=pk)
    form = IsStaffForm(instance=instance)
    if request.method == 'POST':
        form = IsStaffForm(data=request.POST, instance=instance)
        if form.is_valid():
            form.save()
            messages.success(request, 'Status staff berhasil diubah')
            return redirect('user:user_per_verifikator')
        else:
            form = IsStaffForm()
            messages.warning(request, 'Status staff tidak berhasil diubah')

    content = {
        'form': form,
        'instance': instance,
    }
    return render(request, 'staff/edit_user_verifikator.html', content)

