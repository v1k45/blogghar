from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404


def user_profile(request, username):
    # getting default user model
    UserModel = get_user_model()
    profile = get_object_or_404(
        UserModel.objects.select_related(), username=username
    ).profile
    return render(request, 'authapp/user_profile.html', {'profile': profile})
