from django.shortcuts import render, redirect
import random
import string
from django.conf import settings
from django.core.mail import send_mail


from django.template.loader import render_to_string
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

from .forms import SignUpForm
from .models import UserManagement

# Create your views here.


@login_required
def home(request):
    return render(request, "home.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        print(username, password)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page or home page
            return redirect(reverse("home"))
        else:
            # Authentication failed, show error message
            messages.error(request, "Invalid username or password.")

    # If request method is not POST or authentication failed, render login page
    return render(request, "login.html")


def logout_view(request):
    logout(request)
    return redirect("login")  # Redirect to the home page after logout


def generate_verification_code():
    # Generate a random 6-character alphanumeric code
    return "".join(random.choices(string.ascii_letters + string.digits, k=6))


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_active = False  # Mark user as inactive until email is verified

            user.verification_code = generate_verification_code()
            user.save()

            # send_verification_email(user)

            return render(request, "verify_email.html", {"email": user.email})

        else:
            messages.error(request,form.errors)
            print("else", form.errors)

    else:
        form = SignUpForm()
    return render(request, "signup.html", {"form": form})


def send_verification_email(user):
    subject = "Verify your email address"
    from_email = settings.EMAIL_HOST_USER

    email_content = render_to_string(
        "email_verification.html",
        {"email": user.email, "verification_code": user.verification_code},
    )

    send = send_mail(
        subject,
        None,
        from_email,
        [user.email],
        fail_silently=False,
        html_message=email_content,
    )


# def resend_verification(request):
#     if request.method == "POST":
#         print("hehehehehe", request)
#         print("hehehehehe", request.POST)
#         email = request.POST.get("email2")
#         print("email", email)
#         try:
#             user = UserManagement.objects.get(email=email)
#             user.verification_code = generate_verification_code()
#             user.save()
#             # send_verification_email(user)
#             messages.success(request, "Verification code has been resent successfully.")
#             render(request, "verify_email.html", {"email": user.email})
#         except UserManagement.DoesNotExist:
#             messages.error(request, "No user with this email address exists.")
#             return redirect("resend_verification")
#     return render(request, "verify_email.html")


def verify_email(request):
    if request.method == "POST":
        email = request.POST.get("email")
        verification_code = request.POST.get("verification_code")
        try:
            user = UserManagement.objects.get(
                email=email, verification_code=verification_code
            )
            user.is_active = True
            user.save()
            # Redirect to a success page or login page
            return redirect("login")
        except UserManagement.DoesNotExist:
            print("invalid", verification_code, email)
            messages.error(request, "Invalid Code.")
            return render(request, "verify_email.html")

    else:
        # Render a form for the user to enter their email and verification code
        return render(request, "verify_email.html")
