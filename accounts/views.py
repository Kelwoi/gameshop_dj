from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from .forms import SignUpForm, ProfileForm

def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Акаунт створено ✅")
            return redirect("accounts:profile")
    else:
        form = SignUpForm()
    return render(request, "accounts/signup.html", {"form": form})

@login_required
def profile(request):
    prof = request.user.profile
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=prof)
        if form.is_valid():
            form.save()
            messages.success(request, "Профіль оновлено ✅")
            return redirect("accounts:profile")
    else:
        form = ProfileForm(instance=prof)
    return render(request, "accounts/profile.html", {"form": form, "profile": prof})
