from django.shortcuts import render, get_object_or_404
from . import forms
from . import models
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

# Create your views here.


@login_required()
def view_profile(request):
    all_photographs = models.Photography.objects.filter(user_id=request.user)
    return render(request,
                  'profile/profile.html',
                  {'user': request.user,
                   'all_photographs': all_photographs})


@login_required()
def edit_profile(request):
    if request.method == 'POST':
        user_form = forms.UserEditForm(instance=request.user,
                                       data=request.POST)
        profile_form = forms.ProfileEditForm(instance=request.user.profile,
                                             data=request.POST,
                                             files=request.FILES)
        user_form.save()
        profile_form.save()
        return render(request,
                      'profile/profile.html',
                      {'user': request.user})
    else:
        user_form = forms.UserEditForm(instance=request.user)
        profile_form = forms.ProfileEditForm(instance=request.user.profile)
    return render(request,
                  'profile/edit_profile.html',
                  {'user_form': user_form,
                   'profile_form': profile_form})


def registration(request):
    if request.method == 'POST':
        user_form = forms.UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password1'],)
            new_user.save()
            models.Profile.objects.create(user=new_user,
                                          photo='unknown.jpeg')
            return render(request,
                          'registration/registration_complete.html',
                          {'new_user': new_user})
    else:
        user_form = forms.UserRegistrationForm()
    return render(request,
                  'registration/registration.html',
                  {'user_form': user_form})


@login_required()
def password_change(request):
    if request.method == 'POST':
        password_change = PasswordChangeForm(request.user, request.POST)
        if password_change.is_valid():
            user = password_change.save()
            update_session_auth_hash(request, user)
            messages.success(request,
                             'Your password was successfully updated!')
            return redirect('instagram_profile:password_change')
    else:
        password_change = PasswordChangeForm(request.user)
    return render(request,
                  'registration/password_change.html',
                  {'password_change': password_change})


@login_required()
def detail_photographs(request, pk):
    photography = get_object_or_404(models.Photography,
                                    pk=pk)
    if request.method == 'POST':
        comment_form = forms.CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.photography = photography
            new_comment.save()
            return redirect(photography)
    else:
        comment_form = forms.CommentForm()
    return render(request,
                  'photographs/detail_photography.html',
                  {'photography': photography,
                   'comment_form': comment_form})


@login_required()
def create_photography_form(request):
    if request.method == 'POST':
        photography_form = forms.PhotographyForm(request.POST,
                                                 files=request.FILES)
        if photography_form.is_valid():
            new_photography = photography_form.save(commit=False)
            new_photography.user = request.user
            new_photography.save()
            return redirect('instagram_profile:view_profile')
    else:
        photography_form = forms.PhotographyForm()
    return render(request,
                  "photographs/create_photography.html",
                  {'photography_form': photography_form})
