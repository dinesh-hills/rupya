from django.contrib.auth.forms import UserCreationForm


class RegistrationForm(UserCreationForm):
    password2 = None