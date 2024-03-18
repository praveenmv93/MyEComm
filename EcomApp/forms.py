from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import UserManagement


class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        max_length=254, help_text="Required. Enter a valid email address."
    )
    mobile_no = forms.CharField(max_length=15)

    class Meta:
        model = UserManagement
        fields = (
            "first_name",
            "last_name",
            "email",
            "mobile_no",
            "password1",
            "password2",
        )

        def clean_mobile_number(self):
            mobile_number = self.cleaned_data['mobile_no']
            
            # Regular expression pattern to match the mobile number format
            pattern = r'^\+?1?\d{9,15}$'

            import re
            if not re.match(pattern, mobile_number):
                raise forms.ValidationError("Enter a valid mobile number.")
            
            return mobile_number